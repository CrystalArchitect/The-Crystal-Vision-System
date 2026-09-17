# Celestial Portal — Windows App

WinUI 3 application for Celestial Portal governance system with Windows Hello biometric authentication.

## Architecture

```
CelestialPortal.Windows
├── Services/
│   ├── AuthenticationService.cs       Windows Hello + password auth via UserConsentVerifier
│   └── PortalApiClient.cs              HTTP client for Portal REST API
├── Views/
│   └── MainWindow.xaml + .xaml.cs      XAML UI with auth + decision approval workflows
├── App.xaml + App.xaml.cs             Application entry point
└── Package.appxmanifest               WinUI app capabilities
```

## Key Components

### AuthenticationService
- Detects Windows Hello availability via `KeyCredentialManager.IsSupportedAsync()`
- `AuthenticateWithWindowsHelloAsync()` — prompts user via `UserConsentVerifier.RequestVerificationAsync()`
- Fallback: `AuthenticateWithPasswordAsync()` for environments without biometric
- Stores steward identity (Guid + name) after successful auth

### PortalApiClient
- Async/await HTTP calls to Portal backend at `http://localhost:8000`
- `FetchDecisionAsync(decisionCode)` — GET `/v1/decisions/{code}`
- `ApproveDecisionAsync(decisionId, stewardId, voiceHash)` — POST `/v1/admin/stamp`
- `FetchAuditChainAsync(decisionId)` — GET `/v1/audit-chain/{id}`
- JSON serialization with snake_case property naming
- Exception handling with debug output

### MainWindow
- **Authentication View**: Windows Hello button, password fallback, error display
- **Dashboard View**: Decision selector (ComboBox), decision display card, voice approval section, approve button
- **State Management**: Visual state manager for auth/dashboard transitions
- **Event Handlers**:
  - `WindowsHelloButton_Click` → biometric auth
  - `PasswordButton_Click` → password auth
  - `DecisionComboBox_SelectionChanged` → fetch decision from Portal
  - `ApproveButton_Click` → submit approval
  - `RecordButton_Click` → toggle voice recording UI (scaffolding)
  - `LogoutButton_Click` → clear session

## Build & Run

### Prerequisites

- Windows 10 22H2 or later (Windows 11 recommended)
- Visual Studio 2022 with C# / WinUI development workload
- .NET 9.0 SDK
- Celestial Portal running at `http://localhost:8000`

### Build

```bash
# From repository root
dotnet build apps/windows/CelestialPortal.Windows/CelestialPortal.Windows.csproj

# Or from Visual Studio
# Open CelestialPortal.Windows.csproj and Build > Build Solution
```

### Run

```bash
# Development mode (F5 in Visual Studio)
dotnet run --project apps/windows/CelestialPortal.Windows/

# Command line
cd apps/windows/CelestialPortal.Windows
dotnet run
```

### Package (MSIX for Store/Sideload)

```bash
# Visual Studio: Project > Publish > Create App Packages (or Publish)
# Generates .msix file for deployment
```

## API Integration

The app connects to Portal at `http://localhost:8000`. Configure with `PORTAL_URL` env var:

```bash
set PORTAL_URL=https://portal.example.com:8000
dotnet run
```

## Windows Hello Behavior

- **Available**: `UserConsentVerifier.RequestVerificationAsync()` shows Windows Hello prompt (biometric or PIN)
- **Not Available**: Button disabled; user falls back to password
- **Scenarios**: Laptop with infrared camera (face), phone with fingerprint, PC with TPM (PIN)

### Possible Responses

| Result | Meaning |
|--------|---------|
| `Verified` | User approved via biometric/PIN; steward authenticated |
| `Canceled` | User canceled the prompt |
| `NotAvailable` | Windows Hello not configured |
| `DeviceBusy` | Another verification in progress |
| `RetriesExhausted` | Too many failed attempts; locked out temporarily |
| `DeviceNotPresent` | Biometric device unavailable |

## Voice Approval (Scaffolding)

`RecordButton` toggles UI state between "Start Recording" and "Stop Recording". Actual audio capture (microphone, speech-to-text, Portal voice submission) will be implemented with:

- Windows Audio APIs (NAudio or Windows.Media.Audio)
- Whisper client (speech-to-text)
- Portal `/v1/admin/stamp` with `voice_signature_hash`

See `backend/README.md` § Voice Chat Integration.

## Portal API Contract

### Fetch Decision

```
GET /v1/decisions/{decision_code}
Response: { decision_id, decision_code, title, status, event_hash, created_at, approved_by }
```

### Approve Decision

```
POST /v1/admin/stamp
Body: { decision_id, steward_id, voice_signature_hash? }
Response: { decision_id, decision_code, title, status, event_hash, created_at, approved_by }
```

### Audit Chain

```
GET /v1/audit-chain/{decision_id}
Response: [{ event_id, event_category, actor_steward_id, outcome, event_hash, previous_hash, created_at }, ...]
```

## Troubleshooting

**"Windows Hello not available"**
- Device does not support Windows Hello; enable via Settings > Accounts > Sign-in options
- Or fall back to password

**"Portal connection failed"**
- Verify Portal is running: `curl http://localhost:8000/health`
- Check network: `ping localhost`
- Firewall may block; allow port 8000

**"Failed to approve decision"**
- Check Portal logs: `docker-compose logs portal`
- Verify decision exists: `curl http://localhost:8000/v1/decisions/ADM-001`
- Check steward_id matches an enrolled steward in Vault

## Next Steps

1. Implement real audio capture (microphone input)
2. Integrate Whisper speech-to-text
3. Add decision history/audit view
4. Support multiple Portal environments (dev/staging/prod)
5. Implement auto-lock (lock app after inactivity)
6. Add dark/light theme support
7. Certificate pinning for HTTPS Portal connections
8. Multi-workspace support (workspace selector)

## License

MIT — See `LICENSE` in repository root.
