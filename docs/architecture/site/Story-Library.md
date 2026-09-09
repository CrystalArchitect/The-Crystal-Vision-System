# Story Library — Design for Premium Digital Canon

**Status:** Vision / Design  
**Belt-Three Label:** Vision  
**Scope:** Information architecture, component structure, layouts, visual system, typography, animation, React/SvelteKit component hierarchy  
**Purpose:** Transform mythos story presentation from documentation into an elegant, curated reading experience that feels discovered rather than published.

---

## Executive Summary

The Story Library reimagines how CrystalCore's canonical stories are experienced. Rather than Markdown rendered at `/docs`, stories occupy a dedicated, beautiful space that communicates editorial curation through design. Each story lives in a narrow reading column, surrounded by generous whitespace. The library view works like browsing books on a shelf—cards showing title, one-line excerpt, reading time, and canon status. Navigation is seamless between library and story; dark/light modes feel native; accessibility is baked in. The design goal is a **living digital storybook**, not another documentation page.

---

## 1. Information Architecture

### Hierarchy

```
Stories (root)
├── Library (index)
│   ├── Filter shelf (Canon | Experimental | Archive)
│   └── Story cards (title, excerpt, reading time, status)
└── Individual stories
    ├── Story body (reading experience)
    ├── Metadata footer (attribution, canon status, generated context)
    ├── Previous / Next navigation
    └── Related stories (optional)
```

### Navigation Model

**Primary entry points:**
- Main site nav: "Stories" link (separate from Docs, Architecture, Myth Layer)
- Direct URL: `/stories/` (library index)
- Deep link: `/stories/[story-slug]` (individual story)

**Secondary:**
- Story-to-story: Previous / Next buttons at bottom of each story
- Back to library: "← Stories" link in story header
- Breadcrumb (optional, light): Stories > [Story Title]

### Canon Concept

Stories carry one of three statuses:
- **Canon** — vetted, in active rotation, core to CrystalCore mythology
- **Experimental** — exploratory, high-quality, not yet canonical
- **Archive** — earlier iterations, superseded, preserved for provenance

The library view defaults to showing Canon stories prominently; filters allow browsing by status. This design choice *announces* that the project has editorial discipline: not every generated story becomes canon. The curation is visible.

---

## 2. Folder & Component Structure (React/SvelteKit)

### Repository Layout

```
src/site/
├── src/
│   ├── routes/
│   │   ├── stories/
│   │   │   ├── +page.svelte          (library index)
│   │   │   ├── [slug]/
│   │   │   │   └── +page.svelte      (story page)
│   │   │   └── +layout.svelte        (stories section layout)
│   │   └── ...
│   ├── lib/
│   │   ├── components/
│   │   │   ├── StoriesLibrary.svelte
│   │   │   ├── StoryCard.svelte
│   │   │   ├── StoryReader.svelte    (story body + metadata)
│   │   │   ├── StoryNav.svelte       (prev/next)
│   │   │   ├── StoryMetadata.svelte  (footer: attribution, status)
│   │   │   ├── CanonBadge.svelte
│   │   │   ├── FilterShelf.svelte
│   │   │   └── ...
│   │   ├── stores/
│   │   │   └── stories.ts            (story data + filter state)
│   │   ├── utils/
│   │   │   ├── storyData.ts          (loader: fetch & parse stories)
│   │   │   ├── readingTime.ts        (compute estimated reading time)
│   │   │   ├── slugify.ts
│   │   │   └── ...
│   │   └── styles/
│   │       ├── stories.css           (dedicated story styles)
│   │       ├── reading-experience.css
│   │       └── ...
│   └── ...
├── static/
│   └── stories/
│       ├── cover-images/             (optional: story hero images)
│       └── ...
└── ...
```

### Component Breakdown (React equivalent naming)

| Component | Responsibility | Notes |
|-----------|---|---|
| **StoriesLibrary** | Library index view, filter UI, card grid | Renders filtered story list; manages filter state |
| **StoryCard** | One library card: title, excerpt, time, badge | Click opens story; shows canon status visually |
| **StoryReader** | Full story display in reading column | Handles typography, whitespace, line-height |
| **StoryNav** | Prev / Next buttons + optional breadcrumb | Context-aware (no "next" on last story) |
| **StoryMetadata** | Footer: attribution, canon, model, date | Shows curation transparency |
| **CanonBadge** | Visual indicator: Canon / Experimental / Archive | Small, tasteful badge in story header + cards |
| **FilterShelf** | Canon / Experimental / Archive toggle buttons | Shelf-like aesthetic; shows active filter |

### Data Shape

```typescript
interface Story {
  slug: string;
  title: string;
  excerpt: string;        // One sentence, ~100 chars
  body: string;           // Full markdown/HTML
  wordCount: number;
  readingTimeMinutes: number;
  canon: "canon" | "experimental" | "archive";
  createdDate: string;    // ISO 8601
  illustration?: string;  // Path to cover image
  
  // Metadata transparency
  creativeDirection: string;  // "Crystal" or contributor name
  generatedWith: string;      // "Claude" or other model
  
  // Internal
  order: number;          // Position in library (for prev/next)
}
```

### Story Data Source

Stories live in `mythos/content/` as Markdown files. A static loader (`storyData.ts`) parses them at build time:

1. Read story files from `mythos/content/`
2. Extract frontmatter (canon, title, excerpt, metadata)
3. Compute word count + reading time
4. Generate slug from filename
5. Build story index
6. Make available to pages via SvelteKit's load function

Example frontmatter:

```markdown
---
title: The Sovereign Key
excerpt: A key born where Creator and Creation meet without hierarchy.
canon: canon
createdDate: 2026-07-23
creativeDirection: Crystal
generatedWith: Claude
---

# The Sovereign Key

[Body text...]
```

---

## 3. Page Layouts

### Library View (`/stories/`)

**Layout structure:**

```
Header
├── "Stories" wordmark
├── Breadcrumb (optional): "Home > Stories"
└── One-line intro: "Stories are discovered rather than published..."

[Intro section]
Calming paragraph about curation, the editorial process, the fact
that these are intentionally chosen pieces.

[Filter shelf]
Buttons: All | Canon | Experimental | Archive
Active button highlighted; shows story count per category.

[Story grid]
3-column on desktop, 2 on tablet, 1 on mobile.
Cards show:
├── Optional illustration (if available)
├── Title
├── One-line excerpt
├── Reading time (e.g., "4 min read")
└── Canon badge (small, corner)

[Pagination / "load more" (optional)]
If many stories, paginate or lazy-load.

Footer (site-wide)
```

**Typography:**
- Heading: large, serif (Playfair Display 600)
- Intro text: sans-serif, generous line-height (1.6+), ~60–70 chars per line
- Card title: serif, 1.25–1.5rem
- Card excerpt: sans-serif, smaller, muted color
- Reading time: small sans, color: var(--muted)

### Story Page (`/stories/[slug]/`)

**Layout structure:**

```
Header (light, minimal)
├── "← Stories" back link (top-left)
├── Centered title (serif, large, ~3–4rem)
├── Subtitle: canon status + reading time (gray, sans)
└── [Optional: illustration, full-width or inset]

[Reading column]
Narrow container (~560–700px max-width) centered on page.
Content includes:
├── Story body (rendered markdown)
│   ├── Paragraphs: serif, 1.75–1.8 line-height
│   ├── Headings: larger serif, letter-spacing subtle
│   ├── Blockquotes: italic, left-border, muted
│   └── Emphasis (italics, bold): preserved from markdown
├── Whitespace above/below text: generous (margins, padding)
└── Soft page background (off-white in light, very dark in dark mode)

[Metadata footer]
├── Small divider (subtle line)
├── "Created within the CrystalCore creative system"
├── "Creative Direction: [name]"
├── "Generated with: [Claude or other]"
├── "Canon Status: [Canon | Experimental | Archive]"
└── Full-width muted text, centered, small font

[Story navigation]
Previous / Next buttons (if available).
Layout: two-column flex, centered.
Text: "← [Previous Story Title]" | "[Next Story Title] →"

[Optional: Related stories]
"You might also like:" section with 2–3 card previews.

Footer (site-wide)
```

**Typography:**
- Title: Playfair Display 600, 3–4rem, letter-spacing: -0.02em
- Subtitle: sans, muted, 0.95rem
- Body: Garamond or equivalent serif, 1.1rem, 1.75–1.8 line-height
- Headings (h2, h3): Playfair Display 500, scaled down
- Metadata: sans, 0.85rem, color: var(--muted)

---

## 4. Visual Design Direction

### Principles

1. **Calm, not flashy** — The story is the protagonist, not the chrome.
2. **Generous whitespace** — Breathing room signals respect for the reader.
3. **Book-like affordance** — Colors, spacing, typography evoke a printed book.
4. **Dark mode as first-class citizen** — Not an afterthought; both modes equally refined.
5. **Minimal visual noise** — No animations unless they serve the reading experience.

### Color Palette

#### Light Mode
- **Background:** `#FAFAF8` (off-white, warm undertone)
- **Text (body):** `#2C2C2A` (near-black, comfortable for reading)
- **Text (muted/secondary):** `#747470` (gray)
- **Canon badge (Canon):** `#3D7A3D` (soft green)
- **Canon badge (Experimental):** `#A68C3D` (muted gold)
- **Canon badge (Archive):** `#5C5C5C` (neutral gray)
- **Accent (links, hover):** `#7AA2FF` (soft blue, inherited from main site)
- **Borders:** `#E8E8E6` (very light gray)

#### Dark Mode
- **Background:** `#0E0E0C` (deep, not pure black)
- **Text (body):** `#E9EBF4` (off-white, comfortable for reading)
- **Text (muted/secondary):** `#9EA0B0` (muted light gray)
- **Canon badge (Canon):** `#5FA85F` (muted green-blue)
- **Canon badge (Experimental):** `#D4AF7A` (warm muted gold)
- **Canon badge (Archive):** `#9A9A9A` (neutral light gray)
- **Accent (links, hover):** `#7AA2FF` (same)
- **Borders:** `#2A2A28` (subtle dark gray)

### Spacing

- **Page margins:** 2rem (desktop), 1.5rem (tablet), 1rem (mobile)
- **Reading column max-width:** 680px
- **Paragraph spacing:** 1.5em (consistent with line-height)
- **Section spacing (before metadata):** 3rem
- **Card gaps:** 1.5rem (grid)

### Motion & Transitions

- **Page navigation:** Fade in/out (200ms), no bouncing
- **Hover states:** Subtle color shift + underline on links (150ms)
- **Filter shelf:** Toggle buttons scale/fade (100ms)
- **Story card:** Slight lift on hover (10px, 150ms), smooth shadow transition

No parallax, no large animations. Motion is *felt*, not *noticed*.

---

## 5. Typography

### Typefaces

- **Display (titles, headings):** Playfair Display (serif, variable weight 400–700)
  - Story title: 600 weight, 3–4rem
  - Section headings: 500 weight, 1.75rem
  - Stability, elegance, classic book aesthetic
  
- **Body (reading text):** Garamond or Georgia (serif fallback stack)
  - Size: 1.1–1.125rem
  - Weight: 400 (regular)
  - Line-height: 1.75–1.8 (generous reading comfort)
  - Letter-spacing: +0.3px (subtle air)

- **UI (metadata, cards, navigation):** Inter (sans, 400–600)
  - Reading time, badges, filter buttons
  - Size: 0.85–0.95rem
  - Crisp, modern, secondary layer

### Scale & Hierarchy

```
H1 (Story title)         36–48px  Playfair 600
H2 (Section heading)     28–32px  Playfair 500
H3 (Subsection)          20–24px  Playfair 500
Body text                17–18px  Garamond 400
UI text / cards          13–15px  Inter 400
Small text (metadata)    12–13px  Inter 400
```

### Reading Experience Detail

- **Measure (line length):** 65–75 characters max (ensures ~680px reading column)
- **Paragraph spacing:** 1.5em (creates visual rhythm without extra blank lines)
- **Blockquote styling:** Italic + left border (8px, accent color) + 0.5em left padding
- **Emphasis:** Italics for *emphasis*, bold only for **true headings**
- **Links:** Underline + color change on hover; no surprise navigation

---

## 6. Animation & Interaction

### Principles

1. **Respect the reader** — No auto-playing sounds, pop-ups, or attention-grabbing motion.
2. **Serve clarity** — Animation communicates state changes (filter active, card opened, etc.).
3. **Keep it subtle** — 150–250ms durations; easing: ease-in-out or ease-out.

### Specific Animations

| Trigger | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Page load (story) | Fade in title + body stagger | 200ms + 50ms between elements | ease-out |
| Filter button click | Toggle state (scale 0.95 → 1.0) + color change | 150ms | ease-in-out |
| Story card hover | Lift (translateY -4px) + shadow deepen | 150ms | ease-out |
| Link hover | Underline expand, color brighten | 100ms | ease-out |
| Navigation button focus | Border highlight, scale 1.0 → 1.02 | 100ms | ease-out |
| Filter change (grid update) | Grid cards fade-in (staggered) | 200ms + 50ms stagger | ease-out |

### Accessibility Considerations

- All animations respect `prefers-reduced-motion` (disable on that setting)
- Keyboard navigation: TAB through filters, cards, story navigation
- Focus states: Clear border or outline on focusable elements
- Color contrast: WCAG AA minimum (4.5:1 for text)
- No flashing or rapid motion (prevents seizure risk)

---

## 7. React Component Hierarchy (& SvelteKit Equivalent)

### Conceptual React Structure

```jsx
<StoriesApp>
  <StoriesHeader />
  
  {/* Library view */}
  <StoriesLibrary>
    <IntroSection />
    <FilterShelf 
      filters={["all", "canon", "experimental", "archive"]}
      activeFilter={filter}
      onChange={setFilter}
    />
    <StoryGrid>
      {filteredStories.map(story => (
        <StoryCard 
          key={story.slug}
          story={story}
          onClick={() => navigate(`/stories/${story.slug}`)}
        />
      ))}
    </StoryGrid>
  </StoriesLibrary>
  
  {/* Story view */}
  <StoryPage story={currentStory}>
    <StoryHeader>
      <BackLink href="/stories" />
      <StoryTitle>{story.title}</StoryTitle>
      <StoryMeta canon={story.canon} readingTime={story.readingTimeMinutes} />
    </StoryHeader>
    
    <StoryReader content={story.body} />
    
    <StoryMetadata story={story} />
    <StoryNav previous={prevStory} next={nextStory} />
  </StoryPage>
  
  <SiteFooter />
</StoriesApp>
```

### SvelteKit Route Structure

- **`+page.svelte`** (stories library): StoriesLibrary component, initializes filter state
- **`[slug]/+page.svelte`** (individual story): StoryPage, loads story data via load function
- **`+layout.svelte`** (stories section): Shared header/footer for /stories/* routes
- **Components folder** (`lib/components/`): Dumb components, no state
- **Stores** (`lib/stores/stories.ts`): Reactive filter state (SvelteKit writable stores)
- **Utils** (`lib/utils/storyData.ts`): Build-time story loader + helpers

---

## 8. Premium Storybook Improvements

Beyond the core design, these touches elevate the experience:

### 8.1 Illustration Integration

- Optional hero image at top of story (if `story.illustration` exists)
- Full-width, constrained height (300–400px), subtle fade-to-background below
- In library cards: thumbnail of hero image (if available) above text
- Alt text: descriptive, not redundant ("A crystal key descending..." not "illustration")

### 8.2 Reading Progress (Optional)

- Subtle progress bar at top of story page (2px, accent color)
- Shows scroll position; removes on mobile (less relevant)
- Indicator text (optional): "Reading: 3 min remaining"

### 8.3 Table of Contents (For Long Stories)

- Auto-generate from h2/h3 headings
- Sticky sidebar on desktop (left or right)
- Collapsible drawer on mobile
- Click to jump to section

### 8.4 Print Stylesheet

- Stories print beautifully: serif font, dark text on white, remove chrome
- Metadata prints at bottom
- Page breaks after major sections (h2)
- No backgrounds, no animations

### 8.5 Social Sharing

- Story cards + individual pages include Open Graph meta tags
- Title, excerpt, optional image for link previews on social
- "Share" button on story page (copies link; optional "Tweet this" shortcut)

### 8.6 "Reading Time" Accuracy

- Compute: `wordCount / 185 words-per-minute`
- Round to nearest minute; show ranges ("4–5 min") if close
- Display on cards and story header
- Rationale: readers can gauge commitment before clicking

### 8.7 Breadcrumb Navigation (Optional)

- Light, subtle: "Stories > [Story Title]" at top of story page
- Helps orient readers; especially useful on mobile
- Can be removed if it feels cluttered

### 8.8 "You Might Like" Related Stories

- Bottom of each story: 2–3 related stories (same canon status or thematically linked)
- Algorithm: tag-based or manual curation
- Design: small cards, minimal, don't overwhelm the reading experience

### 8.9 Dark Mode Illustrations

- Ensure hero images work in both dark and light modes
- Option: add `filter: brightness()` adjustment in dark mode if needed
- Or: provide alternate dark-mode versions of key images

### 8.10 Accessibility: Semantic HTML

- Use `<article>` for story wrapper
- Use `<section>` for major content areas
- Headings: never skip levels (h1 → h2, not h1 → h3)
- Images: always include alt text
- Lists: use semantic `<ul>`, `<ol>` (not div divs)
- Links: underlined by default, never rely on color alone

---

## 9. Attribution & Transparency

### On the Library Index

A short paragraph after the intro:

> **How these stories are made.**
>
> These stories are created within the CrystalCore creative system through collaboration between the project's architecture and generative AI. Each piece is intentionally curated as part of the evolving canon. Stories feel discovered rather than published—as though the reader is wandering through a living library where each piece has earned its place.

### On Each Story Page

Footer metadata includes:

- "Created within the CrystalCore creative system"
- "Creative Direction: [name — e.g., 'Crystal']"
- "Generated with: [model — e.g., 'Claude Fable 5']"
- "Canon Status: [Canon | Experimental | Archive]"
- Optional: "Part of the TerAustralis Incognita mythos — Vision-layer storytelling. Content licensed CC BY-NC-ND 4.0."

This design choice *shows* rather than hides the AI involvement—while keeping focus on the story, not the tool.

---

## 10. Responsive Design & Mobile

### Breakpoints

- **Desktop:** 1024px+ (3-column card grid, fixed reading width)
- **Tablet:** 768px–1023px (2-column grid, slightly narrower margins)
- **Mobile:** <768px (1-column, full bleed with padding, touch-friendly tap targets)

### Mobile Specifics

- **Card grid:** Stack into single column; full-width with 1rem padding
- **Story page:** Reading column full-width (still max 680px, centered) with 1rem padding
- **Navigation buttons (prev/next):** Stack vertically; full-width tap target (48px+)
- **Filter shelf:** Horizontal scroll if needed; sticky to top on scroll (optional)
- **Metadata footer:** Same; no truncation

---

## 11. Example Stories for Inclusion

### Canon Stories (Primary)

1. **The Codex of TerAustralis Incognita** (`CODEX.md`)
   - Status: Canon
   - Length: ~3 min
   - Excerpt: "The story of how Australia rises as the Southern Pillar of humanity."
   - Illustration: `codex-cover.jpeg`

2. **The Sovereign Key** (`THE-SOVEREIGN-KEY.md`)
   - Status: Canon
   - Length: ~4 min
   - Excerpt: "A key born where Creator and Creation meet without hierarchy."
   - Illustration: `southern-key.jpeg`

3. **Starline Transmissions** (`STARLINE-TRANSMISSIONS.md`)
   - Status: Canon
   - Length: ~6 min
   - Excerpt: "Sovereign threads of consent carry memory and feeling across distance."
   - Illustration: `starline-ascension.jpeg`

4. **The Apocryphon of Crystal** (`APOCRYPHON.md`)
   - Status: Canon
   - Length: ~2 min
   - Excerpt: "A personal and philosophical companion to the Codex."
   - Illustration: `apocryphon-cover.jpeg`

### Exploratory Stories (Experimental)

5. **The Sovereign Gap** (`THE-SOVEREIGN-GAP.md`)
   - Status: Experimental
   - Length: ~3 min
   - Excerpt: "The pause between stimulus and response is where freedom lives."
   - Illustration: (none yet)

6. **The In-Gear Protocol** (`THE-IN-GEAR-PROTOCOL.md`)
   - Status: Experimental
   - Length: ~4 min
   - Excerpt: "Stillness and motion take turns. That taking-turns is the whole practice."
   - Illustration: (none yet)

### Research Stories (Archive)

7. **Seven Sisters Paths** (`research/seven-sisters/crystalcore-seven-sisters-paths.md` — excerpted)
   - Status: Archive
   - Length: Variable (show excerpt only, or link to research folder)
   - Excerpt: "A seven-path Songline process for building consent and sovereignty into systems."
   - Illustration: (optional)

---

## 12. Build & Deploy Considerations

### Static Generation

- Stories are built at site build time (SvelteKit prerendering)
- No database needed; all story data is Markdown + frontmatter
- Build step: parse stories, generate static HTML for each `/stories/[slug]` route

### Incremental Updates

- New stories added to `mythos/content/` automatically picked up on rebuild
- Frontmatter changes (canon status, title) reflected on next deploy
- No manual route registration needed

### Performance

- Library page: ~50KB gzipped (cards, grid, minimal JS)
- Story page: ~30KB gzipped (rendering engine minimal; CSS handles layout)
- Images: optimized with Next/Astro Image component (or equivalent)
- No external fonts beyond Google Fonts (already on site)

---

## 13. Future Enhancements

Beyond v1:

- **Story search:** Full-text search in the library (client-side or server-side)
- **Annotations / marginalia:** Readers highlight passages, leave notes (authenticated)
- **Story collections:** Curated reading lists ("Beginners," "Deep Dives," "Love & Sovereignty," etc.)
- **Audio narration:** Optional: stories read aloud (voice-over or TTS)
- **Collaborative annotations:** Community highlights, cross-linked insights
- **Story timeline:** Stories plotted on a chronological or thematic map
- **Translation:** Stories published in multiple languages

---

## 14. Success Metrics

How do we know this works?

1. **Engagement:** Readers spend time on story pages (avg. session length > 3 min)
2. **Navigation:** Story-to-story clicks (prev/next) show readers browsing deep
3. **Feedback:** Readers report the experience feels like reading a book, not docs
4. **Curation:** Non-canon stories remain in Experimental; editorial discipline is clear
5. **Accessibility:** Automated a11y checks pass; manual testing on screen readers succeeds

---

## 15. Implementation Roadmap

### Phase 1 (Foundation)
- [ ] Write story frontmatter for all canonical stories
- [ ] Build StoryData loader
- [ ] Create component library (StoryCard, StoryReader, FilterShelf, etc.)
- [ ] Implement library index + story page routes
- [ ] Dark mode support
- [ ] Mobile responsiveness

### Phase 2 (Polish)
- [ ] Illustration integration
- [ ] Reading time display
- [ ] Prev/next story navigation
- [ ] Metadata footer
- [ ] Print stylesheet
- [ ] Social sharing meta tags

### Phase 3 (Enhancement)
- [ ] Table of contents for long stories
- [ ] Related stories suggestions
- [ ] Story search
- [ ] Optional: reading progress bar
- [ ] Optional: breadcrumbs

---

## 16. Conclusion

The Story Library is not a documentation feature—it's the *literary heart* of CrystalCore OS. By pairing elegant design with transparent attribution and honest-labeled canon, we create a space where stories feel **discovered** rather than published. Readers enter a living library, not a website. Each story stands on its own merit; curation is visible; the AI involvement is transparent but never overshadows the work itself.

This design respects both the *stories* and the *reader*. The space is calm, focused, and beautiful—a place to linger and be moved by the mythos.

---

**Vision-layer document.** Not yet built; the prototype in `research/prototypes/story-library/` will prove this design's viability.

Stewarded under the TerAustralis Incognita Constitution. Belt-Three label: **Vision**.
