import Foundation

/// Talks to the same FastAPI backend as the web whiteboard (backend/main.py).
/// Point baseURL at your deployed backend - localhost only works if you're
/// running the backend on the same Mac and testing via a Simulator on that
/// Mac; a real iPad needs your Mac's LAN IP or a real deployed host.
struct TutorAPIClient {
    var baseURL = URL(string: "https://YOUR_BACKEND_HOST/api")!

    func startSession(subject: String, topic: String) async throws -> String {
        var request = URLRequest(url: baseURL.appendingPathComponent("session"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(["subject": subject, "topic": topic])

        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(SessionResponse.self, from: data).sessionID
    }

    func registerLiveActivityToken(sessionID: String, token: String) async {
        var request = URLRequest(url: baseURL.appendingPathComponent("session/\(sessionID)/activity-token"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(["token": token])
        _ = try? await URLSession.shared.data(for: request)
    }
}

private struct SessionResponse: Decodable {
    let sessionID: String

    enum CodingKeys: String, CodingKey {
        case sessionID = "session_id"
    }
}
