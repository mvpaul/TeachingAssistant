import Foundation

@MainActor
final class SessionViewModel: ObservableObject {
    @Published var subject = "statics"
    @Published var topic = "free_body_diagrams"
    @Published var sessionID: String?
    @Published var errorMessage: String?

    let api = TutorAPIClient()

    func startSession() async {
        errorMessage = nil
        do {
            let id = try await api.startSession(subject: subject, topic: topic)
            sessionID = id
            // Written to the App Group so the Broadcast Upload Extension
            // (a separate process) knows which session's context to attach
            // uploaded frames to.
            AppGroup.defaults.set(id, forKey: AppGroup.Keys.sessionID)
        } catch {
            errorMessage = "Couldn't start session: \(error.localizedDescription)"
        }
    }
}
