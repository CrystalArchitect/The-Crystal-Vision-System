# Atlas visual QA notes

## Preview
The production preview loads `/atlas` successfully with the title `Celestial Atlas of the Southern Sky — TerAustralis Incognita`.

## Opening view
The opening experience presents a strong two-column composition: large editorial title on the left, dusk-purple “of the Southern Sky” subline, a circular crop of the Night from the Edge artwork on the right, and the `THE SOUTHERN INVISIBLE ATLAS` caption. The VISION seal and atlas-time boundary are visible. The screen retains the Observatory header and footer rather than becoming a disconnected microsite.

## Boundary treatment
The boundary strip is visible before the navigator and explicitly states that the series does not demonstrate extra-spatial compute, a silicon mind, non-local coupling, H1/H2 proof, hardware, or affiliation with named observatories/companies.

## Navigator view
The plate navigator exposes 11 labeled steps: UNNUMBERED / FIRST SKETCH, XXVII / STORM, XXVIII / REBUILT CHART, XXIX / SECOND LOOKING, XXX / ROCKET, PANORAMIC / SOUTHERN EDGE, XXXI / SILENT LINE, XXXII / COEXISTING LAYERS, XXXIII / RECEIVER / CORE, XXXIV / UNFOLDING, XXXV / SILICON BRAIN. The first plate artwork, VISION seal, title, interpretation, boundary note, and previous/next controls are rendered.

## Interaction observation
The browser click attempt on the visible XXVII navigator item did not visibly change the active plate in the returned state; the page remained on the first plate while the viewport moved down to the navigator. This may be a browser annotation/click-target issue, but it should be retested with direct keyboard activation and a second pointer attempt before considering the navigator verified.

## Interaction retest

A direct DOM click was issued against the button whose text contains `XXVII`. The console returned `undefined` rather than the expected active plate state, so the interaction should be treated as unverified in this browser session. The static route, button labels, and initial plate render are verified; the state-switch implementation needs a follow-up test in a normal browser interaction session or with an automated component test.
