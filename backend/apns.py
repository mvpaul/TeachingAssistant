"""
Sends Live Activity push updates via APNs (Apple Push Notification service).

This is what makes tutor feedback show up on the Lock Screen / Dynamic
Island while the student is working in another app (GoodNotes, Notability)
and the iOS host app isn't in the foreground - the Broadcast Upload
Extension can't reliably drive ActivityKit itself, so the backend pushes
the update directly using the token the host app registered.

Requires:
- An APNs Auth Key (.p8) with "Apple Push Notifications service (APNs)"
  enabled, created in the Apple Developer portal under
  Certificates, Identifiers & Profiles > Keys. This needs a paid Apple
  Developer Program membership.
- APNS_TEAM_ID, APNS_KEY_ID, APNS_AUTH_KEY_PATH, APNS_BUNDLE_ID set in .env.

Best-effort by design: failures are logged, never raised, so a missing or
broken APNs configuration never breaks the underlying tutoring response.
"""
import logging
import os
import time
from pathlib import Path
from typing import Optional

import httpx
import jwt

logger = logging.getLogger(__name__)

_TEAM_ID = os.environ.get("APNS_TEAM_ID")
_KEY_ID = os.environ.get("APNS_KEY_ID")
_KEY_PATH = os.environ.get("APNS_AUTH_KEY_PATH")
_BUNDLE_ID = os.environ.get("APNS_BUNDLE_ID")
_ENVIRONMENT = os.environ.get("APNS_ENVIRONMENT", "sandbox")  # "sandbox" while testing via Xcode, "production" for TestFlight/App Store builds

_HOST = "api.sandbox.push.apple.com" if _ENVIRONMENT == "sandbox" else "api.push.apple.com"

_cached_token: Optional[tuple[str, float]] = None


def _bearer_token() -> Optional[str]:
    global _cached_token
    if not (_TEAM_ID and _KEY_ID and _KEY_PATH):
        return None

    if _cached_token and time.time() - _cached_token[1] < 1800:
        return _cached_token[0]

    private_key = Path(_KEY_PATH).read_text()
    token = jwt.encode(
        {"iss": _TEAM_ID, "iat": int(time.time())},
        private_key,
        algorithm="ES256",
        headers={"kid": _KEY_ID},
    )
    _cached_token = (token, time.time())
    return token


async def send_live_activity_update(push_token: str, question: str) -> None:
    """Push a new content-state to a running Live Activity.

    `content-state` keys must match Swift's TutorActivityAttributes.ContentState
    (ios/Shared/TutorActivityAttributes.swift): `question` (String) and
    `updatedAtEpoch` (a plain Unix timestamp, not a Date) - this avoids any
    mismatch with Swift's JSON Date encoding.
    """
    bearer = _bearer_token()
    if not bearer or not _BUNDLE_ID:
        logger.info("APNs not configured - skipping Live Activity push")
        return

    payload = {
        "aps": {
            "timestamp": int(time.time()),
            "event": "update",
            "content-state": {
                "question": question,
                "updatedAtEpoch": time.time(),
            },
        }
    }

    headers = {
        "authorization": f"bearer {bearer}",
        "apns-topic": f"{_BUNDLE_ID}.push-type.liveactivity",
        "apns-push-type": "liveactivity",
        "apns-priority": "10",
    }

    url = f"https://{_HOST}/3/device/{push_token}"
    try:
        async with httpx.AsyncClient(http2=True, timeout=10) as http_client:
            response = await http_client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                logger.warning("APNs push failed: %s %s", response.status_code, response.text)
    except Exception:
        logger.exception("APNs push errored")
