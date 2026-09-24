# Source note — AWS Console Mobile iOS 3.21.0 · KMP / Compose fatal crash

**Filed:** 24 Sep 2026 (Crystal paste — crash summary / RCA)  
**App:** AWSConsoleMobileAppiOS **3.21.0**  
**Class:** Client crash receipt — not Frequency · not PCC · not an exploit playbook

## Crash summary

| Item | Value |
| --- | --- |
| Exception | `EXC_CRASH` (`SIGABRT`) |
| Faulting thread | Thread 0 (main) |
| Termination | `libsystem_c.dylib` → `abort()` |

## Root cause (as analysed)

Unhandled exception in shared **Kotlin Multiplatform / Compose Multiplatform** UI layer:

1. Async path (`invokeCompletion`) converts an `NSError` → Kotlin exception (`Kotlin_ObjCExport_NSErrorAsException`).  
2. Exception travels through `kotlinx.coroutines` and Compose’s `FlushCoroutineDispatcher` (`androidx.compose.ui.platform`).  
3. No catch in the coroutine scope → global Kotlin handler `terminateWithUnhandledException` → intentional process abort.

**One line:** ObjC/`NSError` crossed into Kotlin coroutines on the main Compose dispatcher and was never handled, so KMP aborted the app.

## Sitting relevance

| Lane | Fit |
| --- | --- |
| Cloud / ops hygiene | Mobile console crash = operator tooling fragility neighbour (desk open when AWS UI is in play) |
| Agent / Zero Trust | Reminder that client harnesses fail closed on unhandled async errors — architecture neighbour only |
| Cross-stack | Same KMP/Compose pattern as other multiplatform shells — not CrystalCore |

**Do not:** treat as AWS outage proof · reverse-engineer AWS Console internals · ship a patch PoC against Apple’s/AWS’s binary.

## Confidence

High on the RCA shape (SIGABRT + unhandled Kotlin coroutine → abort) from the pasted stack narrative. Medium without the full `.ips` / symbolicated log in-repo.
