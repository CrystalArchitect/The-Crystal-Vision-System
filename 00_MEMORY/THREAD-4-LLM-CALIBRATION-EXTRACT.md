# Thread 4 extract — LLM calibration in markets

**Canon:** **no**  
**Belt:** research / coordination  
**Working-index ID:** `CVS-T4-CALIB`  
**Domains:** AI Safety (16) → Economics (20)  
**Extracted:** 2026-09-18  
**Sources (in-hub only):** [`CROSS-DOMAIN-THREADS.md`](CROSS-DOMAIN-THREADS.md), [`RESEARCH-STATUS.md`](RESEARCH-STATUS.md), drawer 16/20 INDEX notes  
**Rule:** Extracts, not chat dumps. Connection ≠ merge. Does **not** claim calibration arms finished.

---

## What this bead is

Thread 4 tracks the preregistered LLM-judge calibration experiment (Arm B pinned to `rubric_v1`) and how its curves should correct MiroShark/GTB prediction-market `yes_probability`.

Hub status as of this extract: **in flight** — rubric frozen; results not yet applied to markets. This bead locks the integration contract so markets do not silently treat raw LLM probs as calibrated forecasts.

---

## Contract (hub)

| Step | Status | Owner |
| --- | --- | --- |
| Complete calibration arms (rubric_v1) | In flight (satellite) | Drawer 16 / swarm |
| Extract calibration curves | Blocked on arms | Drawer 16 |
| `yes_probability_corrected = f(raw, curve)` | Design only | Drawer 20 / MiroShark |
| GTB sweeps: raw vs corrected | Blocked on curve | Drawer 20 |
| Compare efficiency / spreads / accuracy | Blocked | 16 + 20 |

**Known market failure mode (already logged in drawer 20):** without contrarian agents, LLM populations make `yes_probability` a sentiment poll, not a forecast. Calibration does not replace lineup balance — both are required.

---

## Integration gap (unchanged)

Prediction markets currently use off-the-shelf LLM estimates. After curves land, prefer committee / rubric_v1-calibrated judges over a single uncalibrated LLM. Do not invent curves in this hub.

---

## Bead links

| Drawer | Path |
| --- | --- |
| 00_MEMORY | this file + [`CROSS-DOMAIN-THREADS.md`](CROSS-DOMAIN-THREADS.md) §Thread 4 |
| 16 | [`../16_AI_SAFETY_RESEARCH/INDEX.md`](../16_AI_SAFETY_RESEARCH/INDEX.md) |
| 20 | [`../20_ECONOMIC_MODELS/INDEX.md`](../20_ECONOMIC_MODELS/INDEX.md) |
| Index | `CVS-T4-CALIB` in [`../00_MASTER_INDEX/WORKING-INDEX.md`](../00_MASTER_INDEX/WORKING-INDEX.md) |

---

<!-- topics: thread-4, llm-calibration, rubric-v1, yes-probability, miroshark -->
