#!/usr/bin/env python3
"""Production sheet for the Crystalwood asset pack."""
import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "assets-web" if MODE == "inline" else "assets-arch")
FONTS = open(os.path.join(HERE, "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()

# Only the two Plex faces are used here; Newsreader is dropped for this sheet.
FONTS = "\n".join(b for b in FONTS.split("\n") if "Newsreader" not in b)

ITEMS = [
    ("coin", "Coin", "Currency", "Soft-round gold bezel, faceted cyan inset. Reads at 32&nbsp;px."),
    ("gem", "Gem", "Currency", "Premium currency. The only item with no metal and no wood."),
    ("potion", "Potion", "Consumable", "Corked flask on the shared octagonal plinth."),
    ("heart", "Heart", "Consumable", "Health pickup. The one asset that breaks palette &mdash; "
     "a pink interior glow rather than cyan."),
    ("sword", "Sword", "Equipment", "Crystal blade, silver crossguard, gem pommel."),
    ("shield", "Shield", "Equipment", "Silver rim, blue field, centred cyan boss."),
    ("crate", "Crate", "Container", "The system&rsquo;s reference object: plank body, eight "
     "corner brackets, cross-brace, latch."),
    ("barrel", "Barrel", "Container", "Same grammar wrapped to a cylinder &mdash; brackets "
     "become hoops."),
    ("chest", "Chest", "Container", "The crate on splayed legs. Reuses the body wholesale."),
    ("key", "Key", "Progression", "Silver shaft, crystal floral bow. Most fragile silhouette "
     "in the set."),
    ("scrolls", "Scrolls", "Progression", "Paired rolls with crystal end-caps on a plinth."),
    ("books", "Books", "Progression", "Stack of four with per-volume spine colours &mdash; the "
     "only lilac in the pack."),
    ("chair", "Chair", "Decor", "Furniture proving the bracket motif scales to thin members."),
    ("lantern", "Lantern", "Decor", "Hanging, with chain. The only asset with a fixing point."),
    ("plant", "Potted Crystal", "Decor", "Bone pot, inset chips, crystal foliage."),
]

PALETTE = [
    ("#cc9c6c", "Wood, mid", "Primary plank fill"),
    ("#84543c", "Wood, shadow", "Plank seams and core shadow"),
    ("#cc8454", "Wood, warm", "Sunlit plank edges"),
    ("#3ccce4", "Crystal, light", "Bracket highlight, gem core"),
    ("#3cb4cc", "Crystal, mid", "Crystal body"),
    ("#cccccc", "Silver, light", "Hardware specular"),
    ("#9c9c9c", "Silver, mid", "Rivets, latches, plinths"),
    ("#848484", "Silver, shadow", "Hardware occlusion"),
    ("#e4e4cc", "Bone", "Paper, pot, book pages"),
    ("#e4b454", "Gold", "Coin only"),
    ("#e46c9c", "Backdrop", "Render ground &mdash; not an asset colour"),
]

CSS = """
__FONTS__
:root{
  --bg:#f1eff4; --card:#fff; --line:#ded9e6; --fg:#1b1823; --muted:#645e75;
  --magenta:#c4356b; --cyan:#1f8ba3; --wood:#8a5a3c; --gold:#9a7016;
  --sans:'IBM Plex Sans',system-ui,-apple-system,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
  --r:10px; --s1:.5rem; --s2:1rem; --s3:1.6rem; --s4:2.6rem; --s5:4.2rem;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#141220; --card:#1d1a2b; --line:#302b44; --fg:#eceaf3; --muted:#a49eb8;
    --magenta:#f2799f; --cyan:#5fd2e8; --wood:#d5a271; --gold:#e4b454;
  }
}
:root[data-theme="dark"]{
  --bg:#141220; --card:#1d1a2b; --line:#302b44; --fg:#eceaf3; --muted:#a49eb8;
  --magenta:#f2799f; --cyan:#5fd2e8; --wood:#d5a271; --gold:#e4b454;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.6;
  -webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--magenta);outline-offset:3px}
.page{max-width:1100px;margin:0 auto;padding:var(--s5) 1.25rem var(--s4)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--magenta);margin:0 0 var(--s2)}
h1{font-size:clamp(2.1rem,5.5vw,3.4rem);line-height:1.04;letter-spacing:-.025em;font-weight:600;
  margin:0 0 var(--s2);text-wrap:balance}
.deck{font-size:1.1rem;color:var(--muted);max-width:60ch;margin:0}
.deck strong{color:var(--fg);font-weight:600}
h2{font-size:1.35rem;font-weight:600;letter-spacing:-.01em;margin:0 0 var(--s2)}
.sect{margin-top:var(--s5)}
.sect-top{border-top:1px solid var(--line);padding-top:var(--s3);margin-bottom:var(--s3)}
.note{color:var(--muted);max-width:64ch;margin:0 0 var(--s2)}

.grid{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.item{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;
  display:flex;flex-direction:column}
.item img{width:100%;height:auto;aspect-ratio:1;object-fit:cover}
.item-body{padding:.85rem .95rem 1rem;display:flex;flex-direction:column;gap:.35rem}
.item h3{margin:0;font-size:1rem;font-weight:600}
.tag{font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--magenta);align-self:flex-start;border:1px solid currentColor;border-radius:99px;
  padding:.15rem .5rem}
.item p{margin:0;font-size:.85rem;color:var(--muted);line-height:1.5}

.swatches{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
.sw{display:flex;gap:.7rem;align-items:center;background:var(--card);border:1px solid var(--line);
  border-radius:8px;padding:.6rem .7rem}
.chip{width:2.1rem;height:2.1rem;border-radius:6px;flex:none;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.sw div{min-width:0}
.sw b{display:block;font-size:.85rem;font-weight:600}
.sw code{font-family:var(--mono);font-size:.7rem;color:var(--muted)}
.sw span{display:block;font-size:.72rem;color:var(--muted);line-height:1.35}

.rules{display:grid;gap:var(--s2);grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
  margin:0;padding:0;list-style:none}
.rules li{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--cyan);
  border-radius:8px;padding:.9rem 1rem}
.rules b{display:block;margin-bottom:.25rem;font-size:.95rem}
.rules span{font-size:.87rem;color:var(--muted)}
.warn li{border-left-color:var(--magenta)}
footer{margin-top:var(--s5);border-top:1px solid var(--line);padding-top:var(--s3);
  color:var(--muted);font-size:.85rem;display:flex;flex-direction:column;gap:.5rem}
footer p{margin:0;max-width:70ch}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def src(name):
    if MODE == "inline":
        return "data:image/jpeg;base64," + b64(os.path.join(WEB, name + ".jpg"))
    return "assets/" + name + ".jpg"


def build():
    items = "".join(
        '<figure class="item"><img src="%s" width="520" height="520" loading="lazy" '
        'decoding="async" alt="Stylised 3D game asset: %s, wood and cyan crystal, on a magenta '
        'backdrop."><figcaption class="item-body"><span class="tag">%s</span><h3>%s</h3>'
        '<p>%s</p></figcaption></figure>'
        % (src(s), t.lower(), g, t, d) for s, t, g, d in ITEMS)

    sw = "".join(
        '<div class="sw"><span class="chip" style="background:%s"></span>'
        '<div><b>%s</b><code>%s</code><span>%s</span></div></div>' % (h, n, h, u)
        for h, n, u in PALETTE)

    return ("""<title>Crystalwood — game asset pack</title>
<style>__CSS__</style>
<div class="page">
  <header>
    <p class="eyebrow">Asset pack · 15 pieces · generated with Grok</p>
    <h1>Crystalwood</h1>
    <p class="deck">A stylised casual-RPG icon set with a single, tightly held design grammar:
      <strong>warm plank wood, cyan crystal, silver hardware</strong>. Fifteen pieces covering
      currency, consumables, equipment, containers, progression and decor &mdash; enough to
      furnish an inventory screen without a gap.</p>
  </header>

  <section class="sect">
    <div class="sect-top"><h2>The set</h2></div>
    <div class="grid">%(items)s</div>
  </section>

  <section class="sect">
    <div class="sect-top"><h2>Palette</h2></div>
    <p class="note">Sampled from the renders themselves &mdash; every pixel outside the backdrop,
      quantised and ranked by frequency across all fifteen images. These are the colours actually
      present, not a guess at intent.</p>
    <div class="swatches">%(sw)s</div>
  </section>

  <section class="sect">
    <div class="sect-top"><h2>Design grammar</h2></div>
    <p class="note">What makes the set cohere. Anything added later should obey these or it will
      read as a different pack.</p>
    <ul class="rules">
      <li><b>Three materials, no more</b><span>Wood, crystal, silver. Gold appears once, on the
        coin. Nothing else enters the set.</span></li>
      <li><b>Crystal is structural, not decorative</b><span>It forms brackets, hoops and bindings
        &mdash; it does the job metal would do in a conventional pack. That inversion is the
        pack&rsquo;s signature.</span></li>
      <li><b>Corner brackets plus rivets</b><span>Eight bracket points and paired silver rivets
        recur on crate, chest, chair and books.</span></li>
      <li><b>One latch design</b><span>The same silver clasp appears on crate, barrel, chest and
        every book in the stack.</span></li>
      <li><b>Octagonal plinth</b><span>Small items &mdash; potion, gem, heart, scrolls &mdash;
        stand on a shared silver base so they sit at a common height.</span></li>
      <li><b>Soft bevels throughout</b><span>No hard edges anywhere. Every corner is rounded,
        which is what keeps the set readable at icon size.</span></li>
      <li><b>Fixed camera</b><span>Consistent three-quarter view, single key light upper-left,
        soft contact shadow. Only the lantern deviates, and only because it hangs.</span></li>
    </ul>
  </section>

  <section class="sect">
    <div class="sect-top"><h2>Before you use these</h2></div>
    <ul class="rules warn">
      <li><b>These are renders, not models</b><span>Flat images from a generator. There is no
        mesh, no UV map and no rig behind any of them. Using them in an engine means either
        treating them as 2D sprites or modelling from them.</span></li>
      <li><b>Every file carries a Grok watermark</b><span>Bottom-right of all fifteen. It must be
        removed or cropped before any shipping use.</span></li>
      <li><b>No alpha channel</b><span>The backdrop is baked in, and it is a radial gradient
        rather than a flat fill &mdash; corner samples range from #bb305b to #d54783. A single
        chroma key will leave a halo; these need per-asset matting.</span></li>
      <li><b>Resolution is 1408&nbsp;&times;&nbsp;1408</b><span>Ample for icons, short of what a
        hero or promotional render would want.</span></li>
      <li><b>Check your generator&rsquo;s terms</b><span>Commercial use of generated imagery
        depends on the terms in force for the account that made it. Worth confirming before these
        reach a storefront.</span></li>
      <li><b>Gaps in the set</b><span>No armour, no food, no ore or crafting material, no
        map/quest item, no negative-state icon (poison, curse). A second pass of six or so would
        close the common inventory categories.</span></li>
    </ul>
  </section>

  <footer>
    <p>Fifteen renders, 1408&nbsp;&times;&nbsp;1408, generated with Grok (xAI). Palette values
      sampled programmatically from the images. Named and grouped by function; the pack came
      without names.</p>
    <p><strong>All rights reserved.</strong> TerAustralis Incognita &mdash; ABN 70 741 068 059.</p>
  </footer>
</div>""" % dict(items=items, sw=sw)).replace("__CSS__", CSS.replace("__FONTS__", FONTS))


DOC = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
"""

if __name__ == "__main__":
    html = build()
    if MODE == "linked":
        html = DOC + html.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n"
        out = os.path.join(HERE, "assets-linked.html")
    else:
        out = os.path.join(HERE, "crystalwood-pack.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.0f KB" % (out, MODE, os.path.getsize(out) / 1024))
