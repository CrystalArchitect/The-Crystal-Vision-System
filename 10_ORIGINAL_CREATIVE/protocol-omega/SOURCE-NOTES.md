# Protocol Omega

## Source capture
- Title: Protocol Omega
- Source: public share-view artifact iframe document, captured without signing in.
- `index.html` includes the frame runtime plus the artifact's inline CSS and inline JavaScript.
- Approximate source size: 57,023 bytes.

## Sections observed
1. Daily bearing plaque: statement, date, daily mark, and streak indicator.
2. What's actually happening: situation, feeling, body location, source, and depth/intensity.
3. Story vs. bearing: story, known truth, and evidence/insistence fields.
4. Set the marker: factual record field.
5. Close the boundary: what is not mine to carry.
6. The ledger: saved entries with expandable details.
7. Footer disclaimer: private record, not a diagnosis, and not evidence beyond the user's own day.

## Share-view save/ledger limitations
- The share view visibly reports: "Saving isn't available in this view right now — the statement below still works, but entries won't be kept. Reopen the page to try again."
- The page showed a sign-in prompt for artifact data, but sign-in was not performed.
- In this view the artifact's `window.claude.use('db')` capability is unavailable, so the daily mark/streak cannot persist, log-entry submission reports that it cannot save, and the ledger cannot read or save data.
- The source contains the full DB-backed logic and UI fallbacks; reopening from an authenticated artifacts list may enable the ledger and persistence.
