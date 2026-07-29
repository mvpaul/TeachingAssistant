import ActivityKit
import Foundation

/// Starts a Live Activity and hands its push token to the backend, which
/// then pushes content-state updates directly via APNs (see
/// backend/apns.py) whenever the extension's uploaded frame gets a new
/// tutor response. This is what surfaces feedback on the Lock Screen (and
/// Dynamic Island, on iPhone) while the student is working in another app,
/// without the host app needing to be running in the foreground.
///
/// Note: Dynamic Island is iPhone-only hardware. On iPad, only the Lock
/// Screen / banner presentation of the Live Activity applies.
@MainActor
final class LiveActivityManager: ObservableObject {
    private var activity: Activity<TutorActivityAttributes>?
    private var tokenTask: Task<Void, Never>?

    func start(subject: String, topic: String, sessionID: String, backend: TutorAPIClient) {
        guard ActivityAuthorizationInfo().areActivitiesEnabled else { return }

        let attributes = TutorActivityAttributes(subject: subject, topic: topic)
        let initialState = TutorActivityAttributes.ContentState(
            question: "Watching your work...",
            updatedAtEpoch: Date().timeIntervalSince1970
        )

        do {
            let activity = try Activity.request(
                attributes: attributes,
                content: .init(state: initialState, staleDate: nil),
                pushType: .token
            )
            self.activity = activity

            tokenTask = Task {
                for await tokenData in activity.pushTokenUpdates {
                    let token = tokenData.map { String(format: "%02x", $0) }.joined()
                    await backend.registerLiveActivityToken(sessionID: sessionID, token: token)
                }
            }
        } catch {
            print("Failed to start Live Activity: \(error)")
        }
    }

    func end() async {
        tokenTask?.cancel()
        await activity?.end(nil, dismissalPolicy: .immediate)
        activity = nil
    }
}
