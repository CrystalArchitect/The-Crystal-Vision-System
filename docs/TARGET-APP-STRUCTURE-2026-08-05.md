# Target app structure — received 2026-08-05

> **Label: Vision.** This document records a *target*, not what runs. The
> `App.tsx` below was supplied by the steward on 2026-08-05 (library-sync
> session, branch `claude/crystalcore-library-sync-x47316`) from a newer
> local build that has not been synced into this repository. It is kept
> here verbatim as the destination structure; the router actually in
> `client/src/App.tsx` is the surveyed state. By the Incognita Rule, the
> two must not be confused.

## Delta: current router → target router

| Piece | In this repository (2026-08-05) | In the target |
|---|---|---|
| `/` Home, `/codex`, `/codex/:collection/:chapter` | present | unchanged |
| `/crystalcore-os` → `pages/Terminal` | **absent** | new route + page |
| `/gallery` → `pages/Gallery` | **absent** | new route + page |
| `contexts/SoundscapeContext` | **absent** | new provider wrapping the app |
| `components/GlobalAudioPlayer` | **absent** | new, rendered beside the router |
| `ThemeProvider defaultTheme` | `"light"` | `"light"` (unchanged) |

To build to target, four modules must be created (`Terminal`, `Gallery`,
`SoundscapeContext`, `GlobalAudioPlayer`) — plus whatever audio assets the
soundscape and player play. Dropping the file below into `client/src/`
today would break the build on those four imports; that is why it is
shelved here instead.

**Terminal groundwork already installed:** the
[`web-os-easter-eggs`](../.claude/skills/web-os-easter-eggs/SKILL.md)
Claude Code skill now lives in this repository (`.claude/skills/`). It
carries the layered-egg design patterns, unlock-state and cinematic
overlay templates, and the browser verification protocol used by the
AERIS-generation terminal — the `/crystalcore-os` page is its intended
consumer. The skill's lore should follow the constellation's canon
conventions (locked names, Starlines/Dreamlines coinages, no Songline
component names).

## Target `App.tsx` (verbatim as received)

```tsx
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { SoundscapeProvider } from "./contexts/SoundscapeContext";
import GlobalAudioPlayer from "./components/GlobalAudioPlayer";
import Home from "./pages/Home";
import Codex from "./pages/Codex";
import CodexReader from "./pages/CodexReader";
import Terminal from "./pages/Terminal";
import Gallery from "./pages/Gallery";


function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/codex"} component={Codex} />
      <Route path={"/codex/:collection/:chapter"} component={CodexReader} />
      <Route path={"/crystalcore-os"} component={Terminal} />
      <Route path={"/gallery"} component={Gallery} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

// NOTE: About Theme
// - First choose a default theme according to your design style (dark or light bg), than change color palette in index.css
//   to keep consistent foreground/background color across components
// - If you want to make theme switchable, pass `switchable` ThemeProvider and use `useTheme` hook

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider
        defaultTheme="light"
        // switchable
      >
        <SoundscapeProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
            <GlobalAudioPlayer />
          </TooltipProvider>
        </SoundscapeProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
```

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059
