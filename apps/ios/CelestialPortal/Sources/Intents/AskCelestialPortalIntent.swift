import AppIntents
import Foundation

/// Siri / Shortcuts entry into Celestial Portal.
/// Uses supported App Intents only — does not replace or bypass Siri.
@available(iOS 17.0, *)
struct AskCelestialPortalIntent: AppIntent {
    static var title: LocalizedStringResource = "Ask Celestial Portal"
    static var description = IntentDescription(
        "Send a request through Celestial Portal into CrystalCore.OS governance."
    )
    static var openAppWhenRun: Bool = false

    @Parameter(title: "Request")
    var utterance: String

    @MainActor
    func perform() async throws -> some IntentResult & ProvidesDialog {
        let client = PortalIntentClient()
        let reply = try await client.ask(utterance: utterance, channel: "siri")
        return .result(dialog: IntentDialog(stringLiteral: reply))
    }
}

@available(iOS 17.0, *)
struct CelestialPortalShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AskCelestialPortalIntent(),
            phrases: [
                "Ask \(.applicationName) \(\.$utterance)",
                "Ask Celestial Portal \(\.$utterance)",
                "Hey \(.applicationName) \(\.$utterance)",
            ],
            shortTitle: "Ask Portal",
            systemImageName: "sparkles"
        )
    }
}

/// Thin HTTP client from App Intent → Portal gateway.
/// Portal forwards to CrystalCore.OS; this client must not call TAI or vendors directly.
@available(iOS 17.0, *)
actor PortalIntentClient {
    // Local compose default; override via app config later.
    private let baseURL = URL(string: "http://127.0.0.1:8000")!

    func ask(utterance: String, channel: String) async throws -> String {
        var request = URLRequest(url: baseURL.appendingPathComponent("v1/gateway/ask"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let body: [String: Any] = [
            "text": utterance,
            "channel": channel,
            "client": "ios.appintent",
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        // Until Portal exposes /v1/gateway/ask, fail soft with a clear message.
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else {
                return "Portal did not respond."
            }
            if http.statusCode == 404 {
                return "Celestial Portal gateway endpoint is not online yet. Open the app to continue."
            }
            guard (200...299).contains(http.statusCode) else {
                return "Portal error (\(http.statusCode))."
            }
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
               let speech = json["speech_text"] as? String {
                return speech
            }
            return String(data: data, encoding: .utf8) ?? "Done."
        } catch {
            return "Could not reach Celestial Portal. Is the device on the same network as the gateway?"
        }
    }
}
