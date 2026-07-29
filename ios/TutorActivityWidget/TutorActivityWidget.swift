import ActivityKit
import SwiftUI
import WidgetKit

/// Renders the Live Activity the host app starts (LiveActivityManager) and
/// the backend updates via push (backend/apns.py). This is the "rich"
/// surfacing channel: it stays visible on the Lock Screen (and Dynamic
/// Island on iPhone) while the student is working in GoodNotes/Notability,
/// without needing the host app in the foreground.
struct TutorActivityWidget: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: TutorActivityAttributes.self) { context in
            lockScreenView(context: context)
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    Image(systemName: "graduationcap.fill")
                }
                DynamicIslandExpandedRegion(.center) {
                    Text(context.state.question)
                        .font(.caption)
                        .lineLimit(3)
                }
            } compactLeading: {
                Image(systemName: "graduationcap.fill")
            } compactTrailing: {
                Text("Tutor")
                    .font(.caption2)
            } minimal: {
                Image(systemName: "graduationcap.fill")
            }
        }
    }

    @ViewBuilder
    private func lockScreenView(context: ActivityViewContext<TutorActivityAttributes>) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Image(systemName: "graduationcap.fill")
                Text("\(context.attributes.subject.capitalized) - \(context.attributes.topic)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Spacer()
            }
            Text(context.state.question)
                .font(.body)
        }
        .padding()
    }
}
