# Story Library Prototype

**Status:** Vision / Working prototype  
**Belt-Three Label:** Vision  
**Scope:** Self-contained HTML/CSS/JS demonstration of the Story Library design

---

## What This Is

A working, self-contained prototype of the premium digital Story Library experience described in `docs/architecture/site/Story-Library.md`. This prototype proves the design's viability and serves as a reference implementation for the SvelteKit/React components that will ship on the live site.

**Run it:** Open `index.html` in any modern browser. No build step needed.

---

## Features Demonstrated

### Library View (`/stories/`)
- Story grid with cards (title, excerpt, reading time, canon status badge)
- Filter shelf: All | Canon | Experimental | Archive
- Responsive grid (3-column desktop, 2-column tablet, 1-column mobile)
- Intro section explaining curation + transparency

### Story Page (`/stories/[slug]/`)
- Narrow reading column (~680px) centered on page
- Typography-focused design (serif body, generous line-height)
- Back link + story title + canon badge + reading time
- Story body with proper heading hierarchy
- Metadata footer (Creative Direction, Generated with, Canon Status)
- Previous / Next story navigation
- Breadcrumb navigation

### Dark Mode
- Full dark mode support; respects system preference
- Both light and dark color palettes defined in CSS
- Smooth theme transitions
- Toggle button to test both modes

### Accessibility
- Semantic HTML (`<article>`, `<section>`, `<nav>`)
- Keyboard navigation (TAB through all interactive elements)
- Focus states on buttons and links
- Color contrast WCAG AA compliant
- Respects `prefers-reduced-motion` media query

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete self-contained prototype (HTML + CSS + JS) |
| `README.md` | This file |

---

## Test the Prototype

### Library Browsing
1. Open `index.html`
2. Click filter buttons: "Canon", "Experimental", "Archive"
3. See story grid update with filtered results
4. Click any story card to open it

### Story Reading
1. Click a story card
2. Read the story in a comfortable, book-like format
3. Use Previous / Next buttons to navigate between stories
4. Click "← Stories" to return to library

### Dark Mode
1. Click the moon/sun button in the header (top-right)
2. Page respects system dark mode preference
3. Try both modes; observe color palette adjusts

### Mobile
1. Resize browser to mobile width (~375px)
2. Grid becomes single-column
3. Navigation buttons stack vertically
4. All text remains readable

---

## Design Principles Demonstrated

1. **Calm, elegant typography** — Serif body text with generous line-height; sans-serif UI layer
2. **Generous whitespace** — Reading column max-width keeps measure comfortable; margins are large
3. **Book-like affordance** — Colors, spacing, and typography evoke a printed book
4. **Minimal visual noise** — Only subtle animations; no distracting effects
5. **Dark mode first-class** — Both modes are equally refined; not an afterthought
6. **Transparent curation** — Canon status is visible; non-canon stories feel exploratory, not excluded
7. **Reading-first experience** — The story is the protagonist; chrome is invisible

---

## Stories Included

All six canonical and exploratory stories from `mythos/content/`:

1. **The Codex** (Canon, 3 min) — The foundational story
2. **The Sovereign Key** (Canon, 4 min) — The key that opens sovereignty
3. **Starline Transmissions** (Canon, 6 min) — The vision of sovereign connection
4. **The Apocryphon** (Canon, 2 min) — Personal, philosophical companion
5. **The Sovereign Gap** (Experimental, 3 min) — The pause as freedom
6. **The In-Gear Protocol** (Experimental, 4 min) — Motion without losing sovereignty

---

## Implementation Notes for SvelteKit/React

### Data Loading
In production, story data will load from `mythos/content/` via a build-time loader. The prototype uses inline story objects; the real implementation will:

```typescript
// src/lib/utils/storyData.ts
import fs from 'fs';
import { parse } from 'gray-matter';

export async function loadStories() {
  const storiesDir = 'mythos/content';
  const files = fs.readdirSync(storiesDir).filter(f => f.endsWith('.md'));
  
  return files.map(file => {
    const raw = fs.readFileSync(`${storiesDir}/${file}`, 'utf-8');
    const { data, content } = parse(raw);
    return {
      slug: slugify(data.title),
      title: data.title,
      excerpt: data.excerpt,
      body: markdownToHTML(content),
      wordCount: countWords(content),
      canon: data.canon || 'experimental',
      creativeDirection: data.creativeDirection,
      generatedWith: data.generatedWith,
      createdDate: data.createdDate,
    };
  });
}
```

### Component Structure
The prototype's logic maps directly to SvelteKit components:

- **Page:** `src/routes/stories/+page.svelte` (library)
- **Page:** `src/routes/stories/[slug]/+page.svelte` (story)
- **Component:** `StoriesLibrary.svelte` (grid + filters)
- **Component:** `StoryReader.svelte` (reading column)
- **Component:** `FilterShelf.svelte` (filter buttons)
- **Store:** `stories.ts` (filter state)

### Styling
The CSS in the prototype is self-contained for portability. In production:

- Move to scoped `.svelte` files or a shared CSS module
- Use CSS custom properties (already in place) for theme switching
- Consider Tailwind or similar for utility classes (optional)
- Maintain the existing color palette and breakpoints

---

## Next Steps

### For the Live Site
1. **Adapt to SvelteKit:** Convert components to `.svelte` files
2. **Wire story data:** Use real `mythos/content/` files with frontmatter loader
3. **Refine typography:** Confirm font choices (Playfair + Garamond) work at scale
4. **Performance:** Optimize image loading, code-split if needed
5. **Testing:** Accessibility audit (WAVE, axe), mobile testing across devices
6. **Analytics:** Track reading time, filter usage, story popularity (optional)

### For the Prototype
- Add illustration/hero image support
- Implement table of contents for longer stories
- Add "related stories" suggestions
- Test print stylesheet
- Social sharing meta tags (Open Graph)

---

## Accessibility Checklist

- [x] Semantic HTML (article, section, nav)
- [x] Heading hierarchy (h1 → h2, no skipped levels)
- [x] Image alt text (demo only; real images need descriptive alt)
- [x] Link underlines (never rely on color alone)
- [x] Focus states visible on keyboard navigation
- [x] Color contrast WCAG AA (4.5:1 minimum)
- [x] Dark mode support
- [x] Respects `prefers-reduced-motion`
- [x] Touch targets min 44px on mobile
- [x] Keyboard-only navigation works

---

## Browser Support

Tested and working on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 10+)

---

## Belt-Three Label

**Vision-layer prototype.** Not production code; design is real; implementation is proof-of-concept.

This prototype explores the *visual and interaction design* of the Story Library, not the SvelteKit architecture. It serves as a reference for the real implementation and demonstrates that the design goals are achievable.

---

*Stewarded under the TerAustralis Incognita Constitution.*
