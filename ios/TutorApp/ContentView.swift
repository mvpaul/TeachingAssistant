import ReplayKit
import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = SessionViewModel()
    @StateObject private var liveActivity = LiveActivityManager()

    var body: some View {
        NavigationStack {
            Form {
                Section("Problem") {
                    TextField("Subject", text: $viewModel.subject)
                    TextField("Topic", text: $viewModel.topic)
                    // TODO: a document picker to upload the homework PDF once,
                    // stored server-side against the session (backend/main.py
                    // create_session currently only takes subject/topic).
                }

                Section("Watch my work") {
                    if let sessionID = viewModel.sessionID {
                        HStack {
                            BroadcastPickerView(extensionBundleID: "com.yourteam.tutor.BroadcastExtension")
                                .frame(width: 44, height: 44)
                            Text("Tap to start/stop. iOS will show its standard recording indicator the whole time this is active - there's no way around that, see the project README.")
                                .font(.footnote)
                                .foregroundStyle(.secondary)
                        }
                        Text("Session: \(sessionID)")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    } else {
                        Button("Start Session") {
                            Task { await viewModel.startSession() }
                        }
                        if let error = viewModel.errorMessage {
                            Text(error).font(.footnote).foregroundStyle(.red)
                        }
                    }
                }
            }
            .navigationTitle("AI Tutor")
            .task(id: viewModel.sessionID) {
                guard let sessionID = viewModel.sessionID else { return }
                liveActivity.start(
                    subject: viewModel.subject,
                    topic: viewModel.topic,
                    sessionID: sessionID,
                    backend: viewModel.api
                )
            }
        }
    }
}

/// RPSystemBroadcastPickerView is UIKit-only - this wraps it for SwiftUI.
/// `extensionBundleID` must exactly match the BroadcastExtension target's
/// PRODUCT_BUNDLE_IDENTIFIER in project.yml.
struct BroadcastPickerView: UIViewRepresentable {
    let extensionBundleID: String

    func makeUIView(context: Context) -> RPSystemBroadcastPickerView {
        let picker = RPSystemBroadcastPickerView()
        picker.preferredExtension = extensionBundleID
        picker.showsMicrophoneButton = false
        return picker
    }

    func updateUIView(_ uiView: RPSystemBroadcastPickerView, context: Context) {}
}
