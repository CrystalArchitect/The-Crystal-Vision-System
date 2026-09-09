# Atlas test-runner preview QA

The `/atlas/test-runner` route loads successfully from the production preview and renders the expected QA instrument: control bar, dream-circle mode selector, reduced-motion toggle, state-machine navigator, current plate readout, acceptance matrix, and event trace.

The default state is index 0 / unnumbered First Sketch. The dream-circle shows the Night from the Edge local asset, Southern Invisible Atlas label, resting mode, motion-on status, purple ring, and the no-telemetry boundary note. The acceptance matrix begins with 3 of 6 checks marked PASS: opening, navigator inventory, and evidence boundary.

The rendered navigator exposes all 11 entries and native button semantics. The browser interaction attempt using the annotated button index moved the viewport to the navigator but did not visibly change the state in the returned screenshot; this should be treated as an automation-coordinate observation rather than a confirmed application defect. Direct DOM or Playwright interaction should be used for definitive transition testing.

The preview build passes with `npm run build` and the static route is prerendered.
