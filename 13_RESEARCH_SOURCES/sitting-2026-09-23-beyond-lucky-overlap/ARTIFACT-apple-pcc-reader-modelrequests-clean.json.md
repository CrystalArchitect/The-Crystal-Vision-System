# Artifact — Apple PCC Accessibility Reader · modelRequests (clean)

**Sibling:** [`SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md`](SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md)  
**Note:** PCC attestation / crypto node metadata intentionally absent (Crystal omitted).

```json
{
  "modelRequests": [
    {
      "timestamp": 1790283504.508682,
      "identifier": "E79AF6DF-6E63-4572-81F9-AF0CD435DB32",
      "response": "# Analytics Logs\n\nCertain analytics, such as daily diagnostic and usage data, for your device and paired Apple devices will appear here.\n\n## This Device\n\n- Analytics-2026-09-24-170614...session.ips.ca.synced, selected  \n- Analytics-2026-09-24-170618...session.ips.ca.synced, selected  \n- Analytics-2026-09-24-202122...session.ips.ca.synced, selected  \n- Analytics-2026-09-25-004741...session.ips.ca.synced, selected  \n- Analytics-2026-09-25-004805...session.ips.ca.synced, selected",
      "model": "com.apple.fm.language.instruct_server_v2.accessibility_reader_ai.generic",
      "modelVersion": "11.110003.23",
      "useCase": "accessibility.readerAI",
      "clientIdentifier": "com.apple.accessibility.AccessibilityReader",
      "executionEnvironment": "PrivateCloudCompute"
    },
    {
      "timestamp": 1790283534.530267,
      "identifier": "C0A1EE57-1657-4099-8B89-5870D25BFCFE",
      "response": "Selected analytics logs include daily diagnostic and usage data for this device and paired Apple devices, covering sessions from 24–25 September 2026.",
      "model": "com.apple.fm.language.instruct_server_v2.text_summarizer.generic",
      "modelVersion": "11.110003.17",
      "useCase": "summarization.accessibilityReader",
      "clientIdentifier": "com.apple.accessibility.AccessibilityReader",
      "executionEnvironment": "PrivateCloudCompute"
    }
  ]
}
```

User MODEL INPUT (both requests): Analytics Logs screen — five `session.ips.ca.synced` filenames dated 2026-09-24 and 2026-09-25, marked selected.
