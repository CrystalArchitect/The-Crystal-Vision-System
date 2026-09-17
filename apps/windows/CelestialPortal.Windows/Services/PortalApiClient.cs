using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace CelestialPortal.Services;

[JsonSerializable]
public class Decision
{
    [JsonPropertyName("decision_id")]
    public Guid DecisionId { get; set; }

    [JsonPropertyName("decision_code")]
    public string DecisionCode { get; set; } = string.Empty;

    [JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;

    [JsonPropertyName("status")]
    public string Status { get; set; } = string.Empty;

    [JsonPropertyName("event_hash")]
    public string EventHash { get; set; } = string.Empty;

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }

    [JsonPropertyName("approved_by")]
    public Guid? ApprovedBy { get; set; }
}

[JsonSerializable]
public class DecisionPayload
{
    [JsonPropertyName("decision_code")]
    public string DecisionCode { get; set; } = string.Empty;

    [JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;

    [JsonPropertyName("description")]
    public string Description { get; set; } = string.Empty;

    [JsonPropertyName("decision_type")]
    public string DecisionType { get; set; } = string.Empty;

    [JsonPropertyName("payload")]
    public Dictionary<string, object> Payload { get; set; } = new();
}

[JsonSerializable]
public class ApprovalRequest
{
    [JsonPropertyName("decision_id")]
    public Guid DecisionId { get; set; }

    [JsonPropertyName("steward_id")]
    public Guid StewardId { get; set; }

    [JsonPropertyName("voice_signature_hash")]
    public string? VoiceSignatureHash { get; set; }
}

public class PortalApiClient
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    private readonly JsonSerializerOptions _jsonOptions;

    public PortalApiClient(string baseUrl = "http://localhost:8000")
    {
        _baseUrl = baseUrl;
        _httpClient = new HttpClient();
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        };
    }

    public async Task<Decision?> FetchDecisionAsync(string decisionCode)
    {
        try
        {
            var url = $"{_baseUrl}/v1/decisions/{decisionCode}";
            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to fetch decision: {response.StatusCode}");
                return null;
            }

            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Decision>(json, _jsonOptions);
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error fetching decision: {ex.Message}");
            return null;
        }
    }

    public async Task<Decision?> ApproveDecisionAsync(
        Guid decisionId,
        Guid stewardId,
        string? voiceSignatureHash = null)
    {
        try
        {
            var url = $"{_baseUrl}/v1/admin/stamp";
            var request = new ApprovalRequest
            {
                DecisionId = decisionId,
                StewardId = stewardId,
                VoiceSignatureHash = voiceSignatureHash
            };

            var json = JsonSerializer.Serialize(request, _jsonOptions);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync(url, content);

            if (!response.IsSuccessStatusCode)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to approve decision: {response.StatusCode}");
                return null;
            }

            var responseJson = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Decision>(responseJson, _jsonOptions);
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error approving decision: {ex.Message}");
            return null;
        }
    }

    public async Task<List<Dictionary<string, object>>?> FetchAuditChainAsync(Guid decisionId)
    {
        try
        {
            var url = $"{_baseUrl}/v1/audit-chain/{decisionId}";
            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to fetch audit chain: {response.StatusCode}");
                return null;
            }

            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json, _jsonOptions);
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error fetching audit chain: {ex.Message}");
            return null;
        }
    }

    public async Task<bool> HealthCheckAsync()
    {
        try
        {
            var url = $"{_baseUrl}/health";
            var response = await _httpClient.GetAsync(url);
            return response.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Health check failed: {ex.Message}");
            return false;
        }
    }
}
