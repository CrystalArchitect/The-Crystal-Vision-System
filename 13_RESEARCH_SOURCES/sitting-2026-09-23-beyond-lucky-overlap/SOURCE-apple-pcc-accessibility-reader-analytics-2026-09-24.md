# Source note — Apple PCC · Accessibility Reader AI · Analytics Logs extract

**Filed:** 24 Sep 2026 (Crystal paste — full readable extraction)  
**Provenance:** User-supplied clean JSON `modelRequests` only · **PCC attestation bundles + cryptographic node metadata omitted by Crystal**  
**How Crystal got it (standard Apple path — not a hack):**  
1. Opened **Settings → Analytics & Improvements → Analytics Data / Analytics Logs** and selected session files dated 24–25 Sep 2026.  
2. Ran **Accessibility Reader** (Apple Intelligence) on that screen → two PCC calls (reader clean + summary).  
3. Opened / exported an **Apple Intelligence Report** JSON (transparency log Apple writes for AI requests).  
4. Kept readable `modelRequests`; dropped bulky `privateCloudComputeRequests` attestation/crypto.  
**Client:** `com.apple.accessibility.AccessibilityReader`  
**Source UI:** `com.apple.Preferences` → Analytics Logs  
**Execution:** `PrivateCloudCompute`

## What this is

Two Private Cloud Compute model calls fired when Accessibility Reader (or Reader summarisation) processed the **Settings → Analytics Logs** screen on Crystal’s device.

| # | Timestamp | ID | Model | Use case |
| --- | --- | --- | --- | --- |
| 1 | 1790283504.508682 | E79AF6DF-6E63-4572-81F9-AF0CD435DB32 | `…accessibility_reader_ai.generic` v11.110003.23 | `accessibility.readerAI` |
| 2 | 1790283534.530267 | C0A1EE57-1657-4099-8B89-5870D25BFCFE | `…text_summarizer.generic` v11.110003.17 | `summarization.accessibilityReader` |

~30 seconds apart: clean/restructure markdown → then tight summariser.

## Device content that was read (USER INPUT — not secret docs)

Settings copy + five selected analytics session filenames:

```text
Analytics Logs
Certain analytics, such as daily diagnostic and usage data, for your device and paired Apple devices will appear here.
This Device
Analytics-2026-09-24-170614...session.ips.ca.synced, selected
Analytics-2026-09-24-170618...session.ips.ca.synced, selected
Analytics-2026-09-24-202122...session.ips.ca.synced, selected
Analytics-2026-09-25-004741...session.ips.ca.synced, selected
Analytics-2026-09-25-004805...session.ips.ca.synced, selected
```

**Dates on filenames:** 24 Sep 2026 (three) · 25 Sep 2026 (two) — Mid-Autumn Festival morning sessions appear on the 25th stamp.

## Model outputs (as returned)

**Reader AI (markdown clean):**

```markdown
# Analytics Logs

Certain analytics, such as daily diagnostic and usage data, for your device and paired Apple devices will appear here.

## This Device

- Analytics-2026-09-24-170614...session.ips.ca.synced, selected
- Analytics-2026-09-24-170618...session.ips.ca.synced, selected
- Analytics-2026-09-24-202122...session.ips.ca.synced, selected
- Analytics-2026-09-25-004741...session.ips.ca.synced, selected
- Analytics-2026-09-25-004805...session.ips.ca.synced, selected
```

**Summariser (`en_AU`):**

> Selected analytics logs include daily diagnostic and usage data for this device and paired Apple devices, covering sessions from 24–25 September 2026.

## Developer prompts (role — not Crystal’s writing)

Apple ships long fixed developer prompts for:

1. **Accessibility Reader AI** — clutter strip + markdown restructure; preserve wording; AU locale; strip footers / AoC boilerplate when site-wide; titles-only style rules for captions, etc.
2. **Text summariser** — hard word caps by input length; groundedness; no meta openers; `en_AU`.

Full prompt text preserved in Crystal’s paste / optional sibling files if needed. **Do not** treat Apple’s system prompts as TerAustralis voice.

## Sitting relevance

| Lane | Fit |
| --- | --- |
| Phone hygiene / Rossen pegs | Live proof that Reader AI can send Settings chrome + analytics *filenames* through PCC |
| Zero Trust / agent desks | Cloud model + use-case tags + PrivateCloudCompute — architecture neighbour, not an exploit |
| Mid-Autumn / Appin sitting | Calendar neighbour only (25 Sep stamps) — no mythos merge |
| Research receipt | Observed Apple instruct models + versions + client bundle |

**Not:** Frequency VO · not a Demiurge expand · not surveillance of third parties · not PCC crypto reverse-engineering (attestation omitted on purpose).

## Hold / hygiene note for Crystal

Filename list = diagnostic session labels, not the log bodies. If reviewing privacy: Settings → Privacy & Security → Analytics & Improvements is the control surface. Reader AI ran on what was on-screen.

## Confidence

High that this is Accessibility Reader → PCC on Analytics Logs UI. Medium on exact iOS path (Preferences bundle confirmed in SOURCE INFO). Attestation / node crypto **not** filed (omitted upstream).
