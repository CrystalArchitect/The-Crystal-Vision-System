# Source note — Gemini iOS · watchdog 0x8BADF00D (TextKit 2 layout)

**Filed:** 24 Sep 2026 (Crystal paste — crash analysis)  
**App:** Gemini · `com.google.gemini`  
**Device frame (as pasted):** iOS **27.0** · `iPhone17,4`  
**Class:** Client crash receipt — not Frequency · not PCC RE · not a Gemini binary reverse-engineer

## Crash overview

| Item | Value |
| --- | --- |
| Termination | `0x8BADF00D` (watchdog timeout) |
| Meaning | OS killed the app — main thread blocked too long |
| Faulting thread | Thread 0 · `com.apple.main-thread` |

## Root cause (as analysed)

Main-thread freeze during **text insert + TextKit 2 layout**:

1. `insertText:` into a `UITextView` (keyboard / input controller).  
2. Layout calc: `NSTextLayoutManager` / `NSTextLayoutFragment` → `-[UITextView _performTextKit2LayoutCalculation:inSize:]`.  
3. Hang in `NSParagraphArbitrator` (`_firstFitLineBreakContextBeforeIndex:`) + `CFStringFindCharacterFromSet` — heavy line-break / character-set work on a large or awkward string → hitch → watchdog.

**One line:** Pasting or rendering a big chunk of text on the main thread made TextKit 2 lay out forever; iOS killed Gemini.

## Mitigation themes (vendor / general UI — not a Gemini patch)

- Chunk large pastes / markdown / code before the text view sees them.  
- Keep heavy parse / tokenize / format **off** the main thread; only hand finished attributed text to UI.

## Sitting relevance

| Lane | Fit |
| --- | --- |
| Phone hygiene | Second mobile AI-client crash this sitting (after AWS Console KMP) — tooling fragility, not your PCC decode |
| CapCut / ElevenLabs / Grok paste | Neighbour warning when dumping huge handoffs into chat UIs — chunk if a client freezes |
| CrystalVision repo | **Not** Crystal’s app unless a local `UITextView` / Compose surface shows the same pattern |

**Do not:** reverse-engineer Gemini · ship exploit against Google’s binary · treat as Apple Intelligence Report.

## Confidence

High on watchdog + TextKit 2 main-thread story from the pasted RCA. Medium without the full `.ips` in-repo. iOS “27.0” as pasted — keep as source claim.
