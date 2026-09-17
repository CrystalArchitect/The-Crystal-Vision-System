using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Windows.Security.Credentials;
using Windows.Security.Credentials.UI;

namespace CelestialPortal.Services;

public class AuthenticationResult
{
    public bool Success { get; set; }
    public string? ErrorMessage { get; set; }
    public Guid? StewardId { get; set; }
    public string? StewardName { get; set; }
}

public class AuthenticationService
{
    private readonly string _relyingParty = "CelestialPortal";
    private bool _windowsHelloAvailable;
    private string? _currentStewardName;
    private Guid? _currentStewardId;

    public AuthenticationService()
    {
        DetectWindowsHelloCapability();
    }

    public bool IsWindowsHelloAvailable => _windowsHelloAvailable;
    public string? CurrentStewardName => _currentStewardName;
    public Guid? CurrentStewardId => _currentStewardId;

    private void DetectWindowsHelloCapability()
    {
        try
        {
            _windowsHelloAvailable = KeyCredentialManager.IsSupportedAsync().GetAwaiter().GetResult();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Windows Hello detection failed: {ex.Message}");
            _windowsHelloAvailable = false;
        }
    }

    public async Task<AuthenticationResult> AuthenticateWithWindowsHelloAsync()
    {
        if (!_windowsHelloAvailable)
        {
            return new AuthenticationResult
            {
                Success = false,
                ErrorMessage = "Windows Hello is not available on this device"
            };
        }

        try
        {
            var result = await UserConsentVerifier.RequestVerificationAsync("Approve administrative decision");

            if (result == UserConsentVerificationResult.Verified)
            {
                _currentStewardId = Guid.NewGuid();
                _currentStewardName = $"Steward {_currentStewardId.ToString().Substring(0, 8)}";

                return new AuthenticationResult
                {
                    Success = true,
                    StewardId = _currentStewardId,
                    StewardName = _currentStewardName
                };
            }

            return new AuthenticationResult
            {
                Success = false,
                ErrorMessage = result switch
                {
                    UserConsentVerificationResult.NotAvailable => "User consent verification not available",
                    UserConsentVerificationResult.Canceled => "User canceled the verification",
                    UserConsentVerificationResult.DeviceBusy => "Device is busy",
                    UserConsentVerificationResult.RetriesExhausted => "Too many failed attempts",
                    UserConsentVerificationResult.DeviceNotPresent => "Biometric device not present",
                    _ => "Verification failed"
                }
            };
        }
        catch (Exception ex)
        {
            return new AuthenticationResult
            {
                Success = false,
                ErrorMessage = $"Authentication error: {ex.Message}"
            };
        }
    }

    public async Task<AuthenticationResult> AuthenticateWithPasswordAsync(string password)
    {
        try
        {
            // In production, this would validate against a secure credential store
            // For now, accept any non-empty password as a fallback
            if (string.IsNullOrEmpty(password))
            {
                return new AuthenticationResult
                {
                    Success = false,
                    ErrorMessage = "Password cannot be empty"
                };
            }

            _currentStewardId = Guid.NewGuid();
            _currentStewardName = "Steward (Password)";

            return new AuthenticationResult
            {
                Success = true,
                StewardId = _currentStewardId,
                StewardName = _currentStewardName
            };
        }
        catch (Exception ex)
        {
            return new AuthenticationResult
            {
                Success = false,
                ErrorMessage = $"Authentication error: {ex.Message}"
            };
        }
    }

    public void Logout()
    {
        _currentStewardId = null;
        _currentStewardName = null;
    }

    public bool IsAuthenticated => _currentStewardId.HasValue;
}
