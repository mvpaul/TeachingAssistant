import ReplayKit
import UIKit
import UserNotifications

/// Runs as its own sandboxed process while the student has this broadcast
/// active (via the RPSystemBroadcastPickerView in the host app). iOS shows
/// its standard recording indicator for the whole time this is running -
/// there is no supported way to suppress or shrink that, by design.
///
/// To keep this cheap (battery + per-frame API cost), frames are NOT sent
/// on every callback. A lightweight grayscale diff runs on every frame
/// locally; a frame is only uploaded when enough of the screen has changed
/// (i.e. the student is actively writing) AND a minimum cooldown has
/// elapsed since the last upload.
final class SampleHandler: RPBroadcastSampleHandler {

    // MARK: - Tunables

    /// Point this at your deployed backend. localhost will NOT work from a
    /// real device/extension - use your Mac's LAN IP during development,
    /// or a real deployed host.
    private let backendBaseURL = URL(string: "https://YOUR_BACKEND_HOST/api")!

    private let minSecondsBetweenSends: TimeInterval = 3.0
    private let diffThreshold: CGFloat = 0.02 // fraction of sampled pixels that must change
    private let thumbnailSize = CGSize(width: 64, height: 64)
    private let uploadMaxDimension: CGFloat = 900

    // MARK: - State

    private var lastSentAt: Date = .distantPast
    private var lastThumbnail: [UInt8]?
    private let ciContext = CIContext()
    private lazy var urlSession = URLSession(configuration: .ephemeral)

    private var sessionID: String? {
        AppGroup.defaults.string(forKey: AppGroup.Keys.sessionID)
    }

    // MARK: - RPBroadcastSampleHandler

    override func broadcastStarted(withSetupInfo setupInfo: [String: NSObject]?) {
        // Session context (subject/topic/session_id) is written into the
        // App Group by the host app before the broadcast picker is shown -
        // nothing to do here.
        lastThumbnail = nil
        lastSentAt = .distantPast
    }

    override func processSampleBuffer(_ sampleBuffer: CMSampleBuffer, with sampleBufferType: RPSampleBufferType) {
        guard sampleBufferType == .video else { return }
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        guard let thumbnail = downsampledGrayscale(pixelBuffer, to: thumbnailSize) else { return }

        defer { lastThumbnail = thumbnail }

        guard let previous = lastThumbnail else { return } // first frame just primes the baseline
        guard changedFraction(previous, thumbnail) >= diffThreshold else { return }
        guard Date().timeIntervalSince(lastSentAt) >= minSecondsBetweenSends else { return }

        lastSentAt = Date()
        sendFrame(pixelBuffer)
    }

    override func broadcastFinished() {
        lastThumbnail = nil
    }

    // MARK: - Frame diffing (cheap - runs on every frame)

    private func downsampledGrayscale(_ pixelBuffer: CVPixelBuffer, to size: CGSize) -> [UInt8]? {
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        let scaleX = size.width / ciImage.extent.width
        let scaleY = size.height / ciImage.extent.height
        let scaled = ciImage.transformed(by: CGAffineTransform(scaleX: scaleX, scaleY: scaleY))

        guard let cgImage = ciContext.createCGImage(scaled, from: CGRect(origin: .zero, size: size)) else {
            return nil
        }

        let width = Int(size.width)
        let height = Int(size.height)
        var pixels = [UInt8](repeating: 0, count: width * height)
        guard let colorSpace = CGColorSpace(name: CGColorSpace.linearGray),
              let context = CGContext(
                data: &pixels, width: width, height: height,
                bitsPerComponent: 8, bytesPerRow: width,
                space: colorSpace, bitmapInfo: 0
              ) else {
            return nil
        }
        context.draw(cgImage, in: CGRect(origin: .zero, size: size))
        return pixels
    }

    private func changedFraction(_ a: [UInt8], _ b: [UInt8]) -> CGFloat {
        guard a.count == b.count, a.count > 0 else { return 1 }
        var changed = 0
        for i in 0..<a.count where abs(Int(a[i]) - Int(b[i])) > 24 {
            changed += 1
        }
        return CGFloat(changed) / CGFloat(a.count)
    }

    // MARK: - Networking (only on a gated, infrequent subset of frames)

    private func sendFrame(_ pixelBuffer: CVPixelBuffer) {
        guard let sessionID else { return }
        guard let jpegData = jpegData(from: pixelBuffer, maxDimension: uploadMaxDimension) else { return }

        let boundary = "Boundary-\(UUID().uuidString)"
        var request = URLRequest(url: backendBaseURL.appendingPathComponent("analyze-frame"))
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"session_id\"\r\n\r\n\(sessionID)\r\n".data(using: .utf8)!)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"frame\"; filename=\"frame.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(jpegData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        request.httpBody = body

        let task = urlSession.dataTask(with: request) { [weak self] data, _, error in
            guard let data, error == nil,
                  let reply = try? JSONDecoder().decode(TutorReply.self, from: data),
                  let question = reply.question, !question.isEmpty else { return }
            self?.deliver(question: question)
        }
        task.resume()
    }

    private func jpegData(from pixelBuffer: CVPixelBuffer, maxDimension: CGFloat) -> Data? {
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        let scale = maxDimension / max(ciImage.extent.width, ciImage.extent.height)
        let scaled = scale < 1 ? ciImage.transformed(by: CGAffineTransform(scaleX: scale, scaleY: scale)) : ciImage
        guard let cgImage = ciContext.createCGImage(scaled, from: scaled.extent) else { return nil }
        return UIImage(cgImage: cgImage).jpegData(compressionQuality: 0.6)
    }

    // MARK: - Delivering feedback

    /// Two channels, both fired from here:
    /// 1. Write to the App Group so the host app can show it if foregrounded.
    /// 2. A rich local notification, since the extension itself has no UI
    ///    and the student is likely inside GoodNotes/Notability, not this app.
    ///
    /// The richest channel - updating the Live Activity - is NOT done from
    /// here. The backend does it directly via an APNs push after it
    /// generates the reply (see backend/apns.py), which is more reliable
    /// than trying to call ActivityKit from inside this extension.
    private func deliver(question: String) {
        AppGroup.defaults.set(question, forKey: AppGroup.Keys.lastQuestion)
        AppGroup.defaults.set(Date(), forKey: AppGroup.Keys.lastUpdatedAt)

        let content = UNMutableNotificationContent()
        content.title = "Tutor"
        content.body = question
        content.sound = .default
        content.categoryIdentifier = "TUTOR_FEEDBACK"

        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)
    }
}

private struct TutorReply: Decodable {
    let question: String?
    let feedback: String?
}
