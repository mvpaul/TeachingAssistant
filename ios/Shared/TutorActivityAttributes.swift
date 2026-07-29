import ActivityKit
import Foundation

/// Live Activity model, shared by the host app (which starts/ends the
/// Activity) and the widget extension (which renders it).
///
/// `updatedAtEpoch` is a plain Unix timestamp (seconds) rather than `Date`
/// on purpose: the backend sends push updates as raw JSON built in Python
/// (see backend/apns.py), and matching a bare number on both sides avoids
/// any ambiguity around Swift's default Date JSON encoding strategy.
struct TutorActivityAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        var question: String
        var updatedAtEpoch: Double

        var updatedAt: Date {
            Date(timeIntervalSince1970: updatedAtEpoch)
        }
    }

    var subject: String
    var topic: String
}
