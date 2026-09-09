# Crystalwood — game asset pack

Fifteen stylised casual-RPG item renders sharing one design grammar: **warm
plank wood, cyan crystal, silver hardware**.

Open `index.html` from a clone to view the production sheet — the set by
function, the palette, the design rules, and the caveats.

This directory is deliberately **not** in `vision-plates/`. Those images are
catalogued because they make claims that need labelling. These make no claim
about anything — they are production art, and they are catalogued for use
rather than for scrutiny.

## The set

| Asset | Group | Note |
|---|---|---|
| `coin.jpg` | Currency | Gold bezel, faceted cyan inset |
| `gem.jpg` | Currency | Premium currency; no metal, no wood |
| `potion.jpg` | Consumable | Corked flask on the shared plinth |
| `heart.jpg` | Consumable | Health pickup; the one pink interior |
| `sword.jpg` | Equipment | Crystal blade, silver crossguard |
| `shield.jpg` | Equipment | Silver rim, blue field, cyan boss |
| `crate.jpg` | Container | The system's reference object |
| `barrel.jpg` | Container | Same grammar wrapped to a cylinder |
| `chest.jpg` | Container | The crate on splayed legs |
| `key.jpg` | Progression | Silver shaft, crystal floral bow |
| `scrolls.jpg` | Progression | Paired rolls, crystal end-caps |
| `books.jpg` | Progression | Stack of four; the only lilac |
| `chair.jpg` | Decor | Bracket motif at thin-member scale |
| `lantern.jpg` | Decor | The only asset with a fixing point |
| `plant.jpg` | Decor | Bone pot, crystal foliage |

Names and groupings are ours — the pack arrived unnamed.

## Palette

Sampled programmatically from the renders (every non-backdrop pixel, quantised
and ranked across all fifteen), so these are the colours actually present rather
than an estimate of intent.

| Hex | Role |
|---|---|
| `#cc9c6c` | Wood, mid — primary plank fill |
| `#84543c` | Wood, shadow — seams and core shadow |
| `#cc8454` | Wood, warm — sunlit edges |
| `#3ccce4` | Crystal, light — bracket highlight, gem core |
| `#3cb4cc` | Crystal, mid — crystal body |
| `#cccccc` | Silver, light — specular |
| `#9c9c9c` | Silver, mid — rivets, latches, plinths |
| `#848484` | Silver, shadow — occlusion |
| `#e4e4cc` | Bone — paper, pot, pages |
| `#e4b454` | Gold — coin only |
| `#e46c9c` | Backdrop — render ground, not an asset colour |

## Design grammar

Anything added later should obey these or it will read as a different pack.

- **Three materials, no more.** Wood, crystal, silver. Gold appears once.
- **Crystal is structural, not decorative.** It forms the brackets, hoops and
  bindings that metal would normally do. That inversion is the pack's signature.
- **Corner brackets plus paired rivets** recur on crate, chest, chair, books.
- **One latch design** across crate, barrel, chest and every book in the stack.
- **Shared octagonal plinth** under the small items, so they sit at a common
  height.
- **Soft bevels throughout** — no hard edges, which is what keeps them readable
  at icon size.
- **Fixed camera:** three-quarter view, key light upper-left, soft contact
  shadow. Only the lantern deviates, because it hangs.

## Before using these

- **They are renders, not models.** Flat images from a generator — no mesh, no
  UVs, no rig. Engine use means treating them as 2D sprites or modelling from
  them.
- **Every file carries a Grok watermark**, bottom-right. Remove or crop before
  any shipping use.
- **No alpha channel.** The backdrop is baked in and is a *radial gradient*, not
  a flat fill — corner samples run from `#bb305b` to `#d54783`. A single chroma
  key will leave a halo; these need per-asset matting.
- **1408 × 1408 native.** Committed here at 1024 px. Fine for icons, short for
  hero art.
- **Check the generator's terms** for commercial use under the account that
  produced them.

## Gaps

No armour, food, ore or crafting material, map/quest item, or negative-state
icon (poison, curse). A second pass of roughly six would close the common
inventory categories.

---

**All rights reserved.** TerAustralis Incognita — ABN 70 741 068 059.
