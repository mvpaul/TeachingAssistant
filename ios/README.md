# iOS "watch my work" app

Scaffolding for an iPad app that watches homework being worked on in another
app (GoodNotes, Notability, etc.) via a system-wide screen broadcast, and
surfaces Socratic tutoring feedback as a Live Activity + notifications.

**Read this first if you haven't already:** iOS requires a persistent,
non-configurable recording indicator to be visible the entire time a
system-wide broadcast is active. There is no supported way to hide, shrink,
or otherwise minimize it - that's an OS-level privacy control, not an app
setting. This project accepts that constraint and builds around it.

**This code has not been compiled or run.** It was written directly against
documented Apple APIs (ReplayKit, ActivityKit, WidgetKit) in a Linux sandbox
with no Xcode/macOS toolchain available to build or test it. Treat it as a
strong first draft: expect to fix real compiler errors, API version quirks,
and framework details Xcode surfaces that couldn't be checked here.

## What's in here

```
ios/
  project.yml                        # XcodeGen spec - generates the .xcodeproj
  Shared/
    AppGroup.swift                   # shared storage between app + extension
    TutorActivityAttributes.swift    # Live Activity data model
  TutorApp/                          # host app (SwiftUI)
    TutorApp.swift                   # app entry point
    ContentView.swift                # session setup + broadcast picker UI
    SessionViewModel.swift           # talks to backend, starts a session
    TutorAPIClient.swift             # thin HTTP client
    LiveActivityManager.swift        # starts the Live Activity, registers its push token
  BroadcastExtension/                # Broadcast Upload Extension
    SampleHandler.swift              # the actual "watching" - frame diffing + gated uploads
  TutorActivityWidget/               # Live Activity UI
    TutorActivityWidget.swift
    TutorActivityWidgetBundle.swift
```

## How the pieces fit together

1. In the host app, the student sets subject/topic and taps **Start
   Session** -> backend creates a session and returns a `session_id`
   (`POST /api/session`), stored in the shared App Group.
2. The student taps the broadcast picker button and selects this app's
   extension -> iOS starts a system-wide screen broadcast (indicator now
   visible) and launches `BroadcastExtension` as its own process.
3. `SampleHandler` runs a cheap grayscale diff on every incoming frame.
   Only when enough of the screen changed (the student wrote something new)
   *and* a cooldown has passed does it downscale + JPEG-encode the frame and
   POST it to `/api/analyze-frame`.
4. The backend calls Claude with the frame as an image input, gets back a
   Socratic nudge, and:
   - returns it to the extension, which writes it to the App Group and
     fires a rich local notification, and
   - if a Live Activity push token has been registered for this session,
     pushes a content-state update directly via APNs (`backend/apns.py`) -
     this is the "richer" channel that updates the Lock Screen / Dynamic
     Island live, without the host app needing to be in the foreground.
5. The host app starts the Live Activity right after creating the session
   and hands its push token to the backend (`LiveActivityManager` ->
   `POST /api/session/{id}/activity-token`).

## Setup

### 1. Install XcodeGen and generate the project

```bash
brew install xcodegen
cd ios
xcodegen generate
open TutorApp.xcodeproj
```

The `.xcodeproj` is generated, not committed - `project.yml` is the source
of truth. Re-run `xcodegen generate` any time you add/remove files or
change target settings.

### 2. Signing & capabilities (in Xcode, for all three targets)

You'll need a **paid Apple Developer Program account** - App Groups on a
real device, and Live Activity push updates, both require it.

For **TutorApp**, **BroadcastExtension**, and **TutorActivityWidget**:
- Signing & Capabilities -> set your Team.
- Add the **App Groups** capability, and check/add
  `group.com.yourteam.tutor` (must match `ios/Shared/AppGroup.swift` and
  all three `.entitlements` files - change all four together if you rename it).

For **TutorApp** only:
- Add the **Push Notifications** capability (required for Live Activity
  push updates).

### 3. Point the code at your backend

Replace `https://YOUR_BACKEND_HOST/api` in:
- `TutorApp/TutorAPIClient.swift`
- `BroadcastExtension/SampleHandler.swift`

`localhost` will not work from a real device or from the extension process
- use your Mac's LAN IP (e.g. `http://192.168.1.23:8000/api`) while the
backend is running with `uvicorn backend.main:app --reload --host 0.0.0.0
--port 8000`, or a real deployed host.

### 4. APNs key (only needed for Live Activity push updates)

1. developer.apple.com -> Certificates, Identifiers & Profiles -> Keys ->
   **+** -> enable "Apple Push Notifications service (APNs)" -> download
   the `.p8` file (shown once).
2. Note the **Key ID** and your **Team ID**.
3. In the backend's `.env`, set `APNS_TEAM_ID`, `APNS_KEY_ID`,
   `APNS_AUTH_KEY_PATH` (path to the `.p8` file), `APNS_BUNDLE_ID`
   (`com.yourteam.tutor`), and `APNS_ENVIRONMENT=sandbox` while testing via
   Xcode (switch to `production` for TestFlight/App Store builds).

If you skip this, everything else still works - Live Activity updates are
just silently skipped (`backend/apns.py` logs and moves on), and you still
get the App Group write + local notification from the extension.

### 5. Build to a real device

- Broadcast Upload Extensions cannot see other real apps' content from the
  Simulator - you need a real iPad running the real GoodNotes/Notability app.
- Dynamic Island is iPhone-only hardware; on iPad, the Live Activity only
  shows on the Lock Screen / via the Live Activity banner, not a Dynamic
  Island.

## Known gaps / next steps

- No homework PDF upload yet - `POST /api/session` only takes subject/topic.
  Add a document picker in `ContentView` and a way to attach the PDF's
  content to the session context server-side.
- Session state in the backend is an in-memory dict (`SESSIONS` in
  `backend/main.py`) - fine for one process during development, not for a
  real deployment (won't survive a restart, doesn't scale past one worker).
- No auth on any of the new endpoints - anyone who can reach your backend
  URL can post frames or start sessions.
