import Foundation

/// Shared storage between the host app and the Broadcast Upload Extension.
///
/// Must match the "App Groups" capability added to every target in Xcode
/// (Signing & Capabilities > App Groups). If you change this identifier,
/// update it in all three .entitlements files too.
enum AppGroup {
    static let identifier = "group.com.yourteam.tutor"

    static var defaults: UserDefaults {
        // Force-unwrap is intentional: a missing App Group here means the
        // capability isn't configured yet, which should fail loudly.
        UserDefaults(suiteName: identifier)!
    }

    enum Keys {
        static let sessionID = "sessionID"
        static let lastQuestion = "lastQuestion"
        static let lastUpdatedAt = "lastUpdatedAt"
    }
}
