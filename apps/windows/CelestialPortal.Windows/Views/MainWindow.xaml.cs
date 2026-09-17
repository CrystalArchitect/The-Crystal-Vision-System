using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using CelestialPortal.Services;

namespace CelestialPortal.Views;

public sealed partial class MainWindow : Window
{
    private readonly AuthenticationService _authService;
    private readonly PortalApiClient _portalClient;
    private Decision? _currentDecision;
    private Guid? _currentStewardId;

    public MainWindow()
    {
        this.InitializeComponent();
        _authService = new AuthenticationService();
        _portalClient = new PortalApiClient();

        // Configure Windows Hello availability
        if (!_authService.IsWindowsHelloAvailable)
        {
            WindowsHelloButton.IsEnabled = false;
            WindowsHelloButton.Content = "Windows Hello not available";
        }

        ExtendsContentIntoTitleBar = true;
    }

    private async void WindowsHelloButton_Click(object sender, RoutedEventArgs e)
    {
        WindowsHelloButton.IsEnabled = false;
        ErrorText.Visibility = Visibility.Collapsed;

        var result = await _authService.AuthenticateWithWindowsHelloAsync();

        if (result.Success && result.StewardId.HasValue)
        {
            _currentStewardId = result.StewardId;
            ShowDashboard();
        }
        else
        {
            ShowError(result.ErrorMessage ?? "Authentication failed");
            WindowsHelloButton.IsEnabled = true;
        }
    }

    private async void PasswordButton_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrEmpty(PasswordBox.Password))
        {
            ShowError("Please enter a password");
            return;
        }

        var result = await _authService.AuthenticateWithPasswordAsync(PasswordBox.Password);

        if (result.Success && result.StewardId.HasValue)
        {
            _currentStewardId = result.StewardId;
            ShowDashboard();
        }
        else
        {
            ShowError(result.ErrorMessage ?? "Authentication failed");
        }
    }

    private async void DecisionComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (DecisionComboBox.SelectedItem is ComboBoxItem item && item.Tag is string decisionCode)
        {
            LoadingRing.IsActive = true;
            DecisionCard.Visibility = Visibility.Collapsed;
            VoiceApprovalPanel.Visibility = Visibility.Collapsed;

            var decision = await _portalClient.FetchDecisionAsync(decisionCode);

            if (decision != null)
            {
                _currentDecision = decision;
                DecisionTitle.Text = decision.Title;
                DecisionCode.Text = decision.DecisionCode;
                DecisionStatus.Text = decision.Status.ToUpper();
                DecisionHash.Text = decision.EventHash.Substring(0, Math.Min(12, decision.EventHash.Length)) + "…";
                DecisionCard.Visibility = Visibility.Visible;
                VoiceApprovalPanel.Visibility = Visibility.Visible;
                ApproveButton.IsEnabled = true;
                StatusText.Text = "Decision loaded. Ready for approval.";
            }
            else
            {
                StatusText.Text = "Failed to load decision. Check Portal connection.";
                ApproveButton.IsEnabled = false;
            }

            LoadingRing.IsActive = false;
        }
    }

    private async void ApproveButton_Click(object sender, RoutedEventArgs e)
    {
        if (_currentDecision == null || !_currentStewardId.HasValue)
        {
            ShowError("No decision selected or not authenticated");
            return;
        }

        ApproveButton.IsEnabled = false;
        LoadingRing.IsActive = true;
        StatusText.Text = "Submitting approval...";

        var result = await _portalClient.ApproveDecisionAsync(
            _currentDecision.DecisionId,
            _currentStewardId.Value,
            TranscriptText.Text);

        if (result != null)
        {
            StatusText.Text = $"Decision approved! Hash: {result.EventHash.Substring(0, 12)}...";
            DecisionStatus.Text = result.Status.ToUpper();
            ApproveButton.IsEnabled = false;
        }
        else
        {
            ShowError("Failed to approve decision");
            ApproveButton.IsEnabled = true;
        }

        LoadingRing.IsActive = false;
    }

    private void RecordButton_Click(object sender, RoutedEventArgs e)
    {
        if (RecordButton.Content.ToString() == "Start Recording")
        {
            RecordButton.Content = "Stop Recording";
            TranscriptText.Visibility = Visibility.Visible;
            TranscriptText.Text = "[Recording audio...]";
        }
        else
        {
            RecordButton.Content = "Start Recording";
            TranscriptText.Text = "Decision approval recorded via voice.";
        }
    }

    private void LogoutButton_Click(object sender, RoutedEventArgs e)
    {
        _authService.Logout();
        _currentStewardId = null;
        _currentDecision = null;
        PasswordBox.Password = string.Empty;
        TranscriptText.Text = string.Empty;
        DecisionComboBox.SelectedIndex = -1;

        VisualStateManager.GoToState(this, "Unauthenticated", true);
        AuthenticationGrid.Visibility = Visibility.Visible;
        DashboardGrid.Visibility = Visibility.Collapsed;
    }

    private void ShowDashboard()
    {
        VisualStateManager.GoToState(this, "Authenticated", true);
        AuthenticationGrid.Visibility = Visibility.Collapsed;
        DashboardGrid.Visibility = Visibility.Visible;
        StatusText.Text = $"Authenticated as {_authService.CurrentStewardName}";
    }

    private void ShowError(string message)
    {
        ErrorText.Text = message;
        ErrorText.Visibility = Visibility.Visible;
    }
}
