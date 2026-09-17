import SwiftUI
import LocalAuthentication

@main
struct CelestialPortalApp: App {
    @StateObject private var authManager = BiometricAuthManager()
    @StateObject private var portalClient = PortalAPIClient()

    var body: some Scene {
        WindowGroup {
            if authManager.isAuthenticated {
                MainDashboard()
                    .environmentObject(authManager)
                    .environmentObject(portalClient)
            } else {
                AuthenticationView()
                    .environmentObject(authManager)
            }
        }
    }
}

// MARK: - Biometric Authentication Manager

class BiometricAuthManager: NSObject, ObservableObject {
    @Published var isAuthenticated = false
    @Published var stewardId: UUID?
    @Published var stewardName: String?
    @Published var errorMessage: String?
    @Published var biometricType: BiometricType = .none

    private let context = LAContext()

    enum BiometricType {
        case faceID
        case touchID
        case none
    }

    override init() {
        super.init()
        detectBiometricCapability()
    }

    private func detectBiometricCapability() {
        var error: NSError?
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            biometricType = .none
            return
        }

        if context.biometryType == .faceID {
            biometricType = .faceID
        } else if context.biometryType == .touchID {
            biometricType = .touchID
        }
    }

    func authenticateWithBiometric() {
        var error: NSError?
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            errorMessage = error?.localizedDescription ?? "Biometric authentication not available"
            return
        }

        context.evaluatePolicy(
            .deviceOwnerAuthenticationWithBiometrics,
            localizedReason: "Approve administrative decision"
        ) { [weak self] success, error in
            DispatchQueue.main.async {
                if success {
                    self?.isAuthenticated = true
                    self?.stewardId = UUID()
                    self?.stewardName = "Steward Alpha"
                    self?.errorMessage = nil
                } else {
                    self?.errorMessage = error?.localizedDescription ?? "Authentication failed"
                }
            }
        }
    }

    func logout() {
        isAuthenticated = false
        stewardId = nil
        stewardName = nil
    }
}

// MARK: - Portal API Client

class PortalAPIClient: NSObject, ObservableObject {
    @Published var currentDecision: Decision?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let baseURL = "http://localhost:8000"
    private let session = URLSession.shared

    struct Decision: Codable {
        let decisionId: UUID
        let decisionCode: String
        let title: String
        let status: String
        let eventHash: String
        let createdAt: Date
        let approvedBy: UUID?

        enum CodingKeys: String, CodingKey {
            case decisionId = "decision_id"
            case decisionCode = "decision_code"
            case title, status
            case eventHash = "event_hash"
            case createdAt = "created_at"
            case approvedBy = "approved_by"
        }
    }

    func fetchDecision(code: String) async {
        DispatchQueue.main.async {
            self.isLoading = true
            self.errorMessage = nil
        }

        guard let url = URL(string: "\(baseURL)/v1/decisions/\(code)") else {
            DispatchQueue.main.async {
                self.errorMessage = "Invalid URL"
                self.isLoading = false
            }
            return
        }

        do {
            let (data, _) = try await session.data(from: url)
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let decision = try decoder.decode(Decision.self, from: data)

            DispatchQueue.main.async {
                self.currentDecision = decision
                self.isLoading = false
            }
        } catch {
            DispatchQueue.main.async {
                self.errorMessage = "Failed to fetch decision: \(error.localizedDescription)"
                self.isLoading = false
            }
        }
    }

    func approveDecision(
        decisionId: UUID,
        stewardId: UUID,
        voiceSignatureHash: String? = nil
    ) async {
        DispatchQueue.main.async {
            self.isLoading = true
        }

        guard let url = URL(string: "\(baseURL)/v1/admin/stamp") else {
            DispatchQueue.main.async {
                self.errorMessage = "Invalid URL"
                self.isLoading = false
            }
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload = [
            "decision_id": decisionId.uuidString,
            "steward_id": stewardId.uuidString,
            "voice_signature_hash": voiceSignatureHash ?? ""
        ] as [String: Any]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload)
            let (data, response) = try await session.data(for: request)

            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                DispatchQueue.main.async {
                    self.errorMessage = "Server error: invalid response code"
                    self.isLoading = false
                }
                return
            }

            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let decision = try decoder.decode(Decision.self, from: data)

            DispatchQueue.main.async {
                self.currentDecision = decision
                self.isLoading = false
                self.errorMessage = nil
            }
        } catch {
            DispatchQueue.main.async {
                self.errorMessage = "Approval failed: \(error.localizedDescription)"
                self.isLoading = false
            }
        }
    }
}

// MARK: - UI Views

struct AuthenticationView: View {
    @EnvironmentObject var authManager: BiometricAuthManager

    var body: some View {
        VStack(spacing: 30) {
            VStack(spacing: 12) {
                Image(systemName: "shield.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.blue)

                Text("Celestial Portal")
                    .font(.title)
                    .fontWeight(.bold)

                Text("Administrative Governance System")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            .frame(maxHeight: .infinity, alignment: .top)
            .padding(.top, 60)

            VStack(spacing: 16) {
                Button(action: authManager.authenticateWithBiometric) {
                    HStack {
                        Image(systemName: authManager.biometricType == .faceID ? "face.smiling" : "touchid")
                        Text(authManager.biometricType == .faceID ? "Sign in with Face ID" : "Sign in with Touch ID")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .disabled(authManager.biometricType == .none)

                if let error = authManager.errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                        .multilineTextAlignment(.center)
                }
            }
            .padding(.bottom, 60)
        }
        .padding()
    }
}

struct MainDashboard: View {
    @EnvironmentObject var authManager: BiometricAuthManager
    @EnvironmentObject var portalClient: PortalAPIClient

    @State private var selectedDecisionCode = "ADM-001"

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                VStack(alignment: .leading, spacing: 8) {
                    Text("Welcome, \(authManager.stewardName ?? "Steward")")
                        .font(.headline)
                    Text("Approve administrative decisions via voice")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(10)

                // Decision Selector
                Picker("Decision", selection: $selectedDecisionCode) {
                    Text("ADM-001: Linting Standards").tag("ADM-001")
                    Text("ADM-002: Deprecation Status").tag("ADM-002")
                }
                .pickerStyle(.segmented)
                .onChange(of: selectedDecisionCode) { code in
                    Task {
                        await portalClient.fetchDecision(code: code)
                    }
                }

                // Decision Display
                if portalClient.isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity, alignment: .center)
                } else if let decision = portalClient.currentDecision {
                    VoiceApprovalView(decision: decision)
                } else {
                    Text("No decision selected")
                        .foregroundColor(.secondary)
                        .frame(maxHeight: .infinity, alignment: .center)
                }

                // Logout
                Button(action: authManager.logout) {
                    Text("Sign Out")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(10)
                }

                if let error = portalClient.errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                        .multilineTextAlignment(.center)
                }
            }
            .padding()
            .navigationTitle("Portal")
            .onAppear {
                Task {
                    await portalClient.fetchDecision(code: selectedDecisionCode)
                }
            }
        }
    }
}

struct VoiceApprovalView: View {
    let decision: PortalAPIClient.Decision

    @State private var isRecording = false
    @State private var voiceTranscript = ""

    var body: some View {
        VStack(spacing: 16) {
            // Decision Card
            VStack(alignment: .leading, spacing: 12) {
                Text(decision.title)
                    .font(.headline)

                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Label(decision.decisionCode, systemImage: "doc.text")
                        Label(decision.status.uppercased(), systemImage: "checkmark.circle.fill")
                    }
                    .font(.caption)
                    .foregroundColor(.secondary)

                    Spacer()

                    Text(decision.eventHash.prefix(12) + "…")
                        .font(.system(.caption, design: .monospaced))
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(10)

            // Voice Input
            VStack(spacing: 12) {
                Text("Voice Approval")
                    .font(.subheadline)
                    .fontWeight(.semibold)

                Button(action: { isRecording.toggle() }) {
                    HStack {
                        Image(systemName: isRecording ? "mic.fill" : "mic")
                        Text(isRecording ? "Recording…" : "Start Recording")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(isRecording ? Color.red : Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }

                if !voiceTranscript.isEmpty {
                    Text("Transcript: \(voiceTranscript)")
                        .font(.caption)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                }
            }

            Spacer()
        }
    }
}
