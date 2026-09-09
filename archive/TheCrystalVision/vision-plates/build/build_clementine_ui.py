#!/usr/bin/env python3
"""Clementine v1.0 — reading a usable design system out of eight mood mockups."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "cl-web" if MODE == "inline" else "cl-arch")
MAN = json.load(open(os.path.join(HERE, "cl-manifest.json")))
FONTS = open(os.path.join(HERE, "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()

TOKENS = [
    ("#e11d48", "rose", "The person&rsquo;s own messages", "role"),
    ("#38bdf8", "sky", "Clementine&rsquo;s replies", "role"),
    ("#7c3aed", "violet", "Consent and system chrome, version badge", "chrome"),
    ("#f0c14a", "amber", "Local-Only Mode when engaged", "state"),
    ("#12101f", "ground", "App background &mdash; starfield or flat", "surface"),
    ("#1d1a2b", "panel", "Cards and sheets", "surface"),
]

ERRORS = [
    ("&ldquo;Sost Sky-Blue&rdquo;", "Soft Sky-Blue"),
    ("&ldquo;Rose-Scrlot&rdquo;", "Rose-Scarlet"),
    ("&ldquo;Violtht&rdquo;", "Violet"),
    ("&ldquo;Siky Blue&rdquo;", "Sky Blue"),
    ("&ldquo;Outtit&rdquo; / &ldquo;Outfit&rdquo;", "unclear &mdash; possibly Outlet, or a menu label"),
    ("&ldquo;clear lone&rdquo;", "clear skies"),
]

CSS = """
__FONTS__
:root{
  --bg:#0e0c18; --panel:#181524; --line:#2a2540; --fg:#eae7f4; --muted:#948da9;
  --rose:#e11d48; --sky:#38bdf8; --violet:#8b5cf6; --amber:#f0c14a;
  --serif:'Newsreader',Georgia,serif; --sans:'IBM Plex Sans',system-ui,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
  --s2:1rem; --s3:1.7rem; --s4:2.8rem; --s5:4.4rem;
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --bg:#f4f2f8; --panel:#fff; --line:#ddd7e8; --fg:#191527; --muted:#5f5977;
    --rose:#be123c; --sky:#0369a1; --violet:#6d28d9; --amber:#8a6410;
  }
}
:root[data-theme="light"]{
  --bg:#f4f2f8; --panel:#fff; --line:#ddd7e8; --fg:#191527; --muted:#5f5977;
  --rose:#be123c; --sky:#0369a1; --violet:#6d28d9; --amber:#8a6410;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.65;
 -webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--violet);outline-offset:3px}
.page{max-width:1080px;margin:0 auto;padding:var(--s5) 1.25rem var(--s4)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;
 color:var(--violet);margin:0 0 var(--s2)}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(2.3rem,6vw,3.8rem);line-height:1.02;
 letter-spacing:-.025em;margin:0 0 var(--s2);text-wrap:balance}
.deck{color:var(--muted);max-width:64ch;margin:0 0 var(--s2);font-size:1.06rem}
.deck strong{color:var(--fg);font-weight:600}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.6rem,3.4vw,2.2rem);margin:0 0 .3rem;
 letter-spacing:-.015em}
.sect{margin-top:var(--s5);border-top:1px solid var(--line);padding-top:var(--s3)}
.note{color:var(--muted);max-width:66ch;margin:0 0 var(--s3)}
.note strong{color:var(--fg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:var(--s2)}
.grid img{border:1px solid var(--line);border-radius:6px;width:100%;height:auto}
.tok{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.tok div{display:flex;gap:.75rem;align-items:center;background:var(--panel);
 border:1px solid var(--line);border-radius:8px;padding:.65rem .75rem}
.chip{width:2.3rem;height:2.3rem;border-radius:6px;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}
.tok b{display:block;font-size:.9rem}
.tok code{font-family:var(--mono);font-size:.72rem;color:var(--muted)}
.tok span{display:block;font-size:.76rem;color:var(--muted);line-height:1.4}
table{width:100%;border-collapse:collapse;font-size:.9rem}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
th,td{text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--mono);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;
 color:var(--muted);font-weight:500}
tr:last-child td{border-bottom:0}
td.was{font-family:var(--mono);color:var(--rose)}
td.is{font-family:var(--mono);color:var(--sky)}
.rules{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:var(--s2);max-width:68ch}
.rules li{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--violet);
 border-radius:8px;padding:.9rem 1rem}
.rules b{display:block;margin-bottom:.25rem}
.rules span{color:var(--muted);font-size:.92rem}
.warn{border-left-color:var(--rose)!important}
footer{margin-top:var(--s5);border-top:1px solid var(--line);padding-top:var(--s3);
 color:var(--muted);font-family:var(--mono);font-size:.75rem;line-height:1.8}
"""


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def src(n):
    if MODE == "inline":
        return "data:image/jpeg;base64," + b64(os.path.join(WEB, n + ".jpg"))
    return "mockups/" + n + ".jpg"


def build():
    grid = "".join(
        '<img src="%s" width="%d" height="%d" loading="lazy" decoding="async" '
        'alt="Clementine app mockup: a dark chat interface with rose and sky-blue message '
        'bubbles and a Local-Only Mode toggle.">' % (src(k), MAN[k][0], MAN[k][1])
        for k in sorted(MAN))
    tok = "".join(
        '<div><span class="chip" style="background:%s"></span><div><b>%s</b><code>%s</code>'
        '<span>%s</span></div></div>' % (h, n, h, u) for h, n, u, _ in TOKENS)
    errs = "".join('<tr><td class="was">%s</td><td class="is">%s</td></tr>' % (a, b)
                   for a, b in ERRORS)

    return ("""<title>Clementine v1.0 — reading a spec out of the mockups</title>
<style>__CSS__</style>
<div class="page">
  <header>
    <p class="eyebrow">Clementine v1.0 &middot; UI direction &middot; 8 mockups</p>
    <h1>There is a real design system in here. It is not the one written on the mockups.</h1>
    <p class="deck">Eight generated mockups for the Clementine companion app. They are
      <strong>mood and direction, not specification</strong> &mdash; the labels are garbled, the
      hex codes contradict the colours they sit on, and at least one swatch is captioned with a
      blue value while rendering red.</p>
    <p class="deck">Taken as a vibe they are coherent and good. Taken as a spec they will send a
      developer down a hole. This sheet separates the two: what to keep, what the values actually
      are, and what to ignore.</p>
  </header>

  <section class="sect">
    <h2>The mockups</h2>
    <p class="note">Two families: a light iMessage-style chat, and a dark starfield with a
      floating consent card. The dark direction is the stronger one and is the only family that
      shows the consent surface.</p>
    <div class="grid">%(grid)s</div>
  </section>

  <section class="sect">
    <h2>What to keep &mdash; the system underneath</h2>
    <p class="note">Consistent across every mockup regardless of the label errors. This is the
      part worth building from.</p>
    <div class="tok">%(tok)s</div>
  </section>

  <section class="sect">
    <h2>What to fix &mdash; text errors on the sheets</h2>
    <p class="note">Generator artefacts. None of these are design decisions; all of them would be
      copied straight into a build by anyone treating the mockups as reference.</p>
    <div class="wrap"><table>
      <thead><tr><th>On the mockup</th><th>Intended</th></tr></thead>
      <tbody>%(errs)s</tbody>
    </table></div>
    <p class="note" style="margin-top:1.2rem"><strong>The colour labels are worse than the
      spelling.</strong> One sheet puts <code>#3b5cf6</code> &mdash; a blue &mdash; on a red
      bubble. Another puts <code>#8b82f6</code> on a bubble rendered in the same blue as
      <code>#3b82f6</code> beside it. The light-chat family also uses <code>#e74c3c</code> and
      <code>#3b82f6</code>, while the dark family uses <code>#e11d48</code> and
      <code>#38bdf8</code>. <strong>Those are four different colours for two roles.</strong> Pick
      the dark family's pair; it has better contrast on a dark ground and the light family's blue
      fails against its own bubble fill.</p>
  </section>

  <section class="sect">
    <h2>What the UI gets right about the architecture</h2>
    <p class="note">This is the genuinely interesting part, and it is why these are worth keeping
      at all. The interface is expressing real constraints from the project, not decorating them.</p>
    <ul class="rules">
      <li><b>Local-Only Mode is always visible</b><span>It is on the chat screen, the consent
        card, and the settings card &mdash; never buried in a preferences pane. That matches
        local-first as a hard requirement rather than a feature: if the mode can be forgotten, it
        is not a guarantee.</span></li>
      <li><b>Consent Log is a screen, not a checkbox</b><span>Giving consent its own titled
        surface is the interface admission that consent is a runtime property &mdash; revocable
        and inspectable &mdash; rather than a document agreed once at install.</span></li>
      <li><b>Cloud API Keys defaults OFF, next to Local-Only ON</b><span>The two controls are
        adjacent and inversely set. The default state shown is the sovereign one, which is the
        correct fail-safe: local isolation, never fail-open.</span></li>
      <li><b>Version badge on every screen</b><span><code>v1.0</code> sits beside the name
        throughout. Small, and it does the same work as <em>provisional and revisable</em> does
        elsewhere in this project.</span></li>
      <li class="warn"><b>Generate Image / Generate Video sit inside the consent card</b>
        <span>The one thing to reconsider. These are outbound-capable actions placed on the same
        surface as the local-only guarantee, with no indication of which way they route. If they
        can reach a cloud endpoint they belong behind the Cloud API Keys toggle, visibly. If they
        run locally, say so on the button.</span></li>
    </ul>
  </section>

  <section class="sect">
    <h2>Open questions for the build</h2>
    <ul class="rules">
      <li><b>Which family wins?</b><span>The light chat and the dark starfield are different
        products. The dark one carries the consent surface and the identity; the light one is
        generic. Recommend dark, with a light theme derived from it rather than the reverse.</span></li>
      <li><b>What does the microphone button do offline?</b><span>It appears on both phone
        mockups with Local Mode ON. Speech recognition is the most likely thing to silently
        require a network call, so its behaviour under local-only needs deciding before it ships,
        not after.</span></li>
      <li><b>&ldquo;Outfit&rdquo; is unresolved</b><span>It appears top-left on two phone
        mockups in a position that reads like a nav label. If it is a persona or appearance
        switcher, it deserves a real name; if it is generator noise, it should go.</span></li>
    </ul>
  </section>

  <footer>
    Eight mockups generated with Grok (xAI), 784&times;1168. Colour roles and architectural
    readings derived from the images; text corrections are proposed, not authoritative.<br>
    These are direction, not a specification. Nothing here reflects shipped software.<br>
    All rights reserved. TerAustralis Incognita &mdash; ABN 70 741 068 059.
  </footer>
</div>""" % dict(grid=grid, tok=tok, errs=errs)).replace("__CSS__", CSS.replace("__FONTS__", FONTS))


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
        out = os.path.join(HERE, "cl-linked.html")
    else:
        out = os.path.join(HERE, "clementine-ui.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.0f KB" % (out, MODE, os.path.getsize(out) / 1024))
