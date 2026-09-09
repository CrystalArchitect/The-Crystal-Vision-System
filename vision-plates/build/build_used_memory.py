#!/usr/bin/env python3
"""Campaign sheet for USED MEMORY — a fictional film, in three treatments."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "um-web" if MODE == "inline" else "um-arch")
MAN = json.load(open(os.path.join(HERE, "um-manifest.json")))
FONTS = open(os.path.join(HERE, "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()

SECTIONS = [
    dict(key="original", n="01", title="Theatrical, Christmas 1984",
         sub="Parallax Pictures", cls="",
         lede="The prestige one-sheet. Airbrushed portrait floating over a night skyline, "
              "chrome-bevel title, and the tagline set in serif italic: "
              "<em>Every memory has its price.</em> Everything about it says a studio believed "
              "in this picture.",
         obs=["The four passes are a billing-block study. Each iteration tightens the credit "
              "line — cast order shifts, the music and photography credits find their place, and "
              "by the last pass the block reads like a real one: distributor, presenting credit, "
              "film-by, five names, then the below-the-line stack in decreasing point size.",
              "The neural ports on the temple are the only science-fiction element on the sheet. "
              "Restraint of exactly the kind 1984 marketing actually used &mdash; sell the face, "
              "hint at the premise."]),
    dict(key="rerelease", n="02", title="Re-edited special version",
         sub="Coronet Releasing &middot; now on a double bill", cls="red",
         lede="The same film after the distributor got hold of it. Cream stock, blackletter-heavy "
              "condensed sans in postbox red, halftone grain, corner wear. "
              "<strong>Faster. Meaner. 84 minutes. The way the street wanted it.</strong>",
         obs=["An 84-minute cut is the whole story in one number. Something was taken out, and "
              "the poster is bragging about it.",
              "The dreaming woman is gone entirely. The campaign no longer sells memory as loss "
              "&mdash; it sells a man running down a wet street. Same footage, opposite promise.",
              "The four passes move the title from top to bottom and back, testing whether the "
              "logo or the image leads. Pass 3, with the tagline wedged above the title, is the "
              "one that reads most like a real grindhouse re-issue."]),
    dict(key="cast", n="03", title="Cast sheet", sub="Four principals",
         cls="grey",
         lede="Production stills in a 2&times;2 contact grid, shot like a casting book: flat grey "
              "seamless, available light, no glamour.",
         obs=["Four characters, and they recur with real consistency across every variant &mdash; "
              "the man in the torn work jacket with a hospital wristband; the technician in a "
              "leather apron with a magnifier band pushed up on her forehead; the broker in a "
              "worn suit, gold-toothed, grinning; the donor with electrodes at her temple.",
              "Two props do the continuity work. The <strong>hospital wristband</strong> says the "
              "man has been processed by something. The <strong>origami crane</strong> on the "
              "broker's table is the only soft object in his frame, and it is folded from the "
              "kind of paper a receipt is printed on.",
              "What changes between passes is the technician's headband sticker &mdash; a teddy "
              "bear, then a rocket, then flowers. A person who decorates her safety equipment. "
              "That is characterisation done with a sticker."]),
]

CSS = """
__FONTS__
:root{
  --ink:#0a0d16; --card:#131826; --line:#242c42; --fg:#e9ecf5; --muted:#8d96b0;
  --chrome:#b9c6e0; --red:#d8342a; --cream:#e8e0cf;
  --serif:'Newsreader',Georgia,serif; --sans:'IBM Plex Sans',system-ui,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
  --s2:1rem; --s3:1.7rem; --s4:2.8rem; --s5:4.5rem;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--ink);color:var(--fg);font-family:var(--sans);line-height:1.65;
 -webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--chrome);outline-offset:3px}
.page{max-width:1120px;margin:0 auto;padding:var(--s5) 1.25rem var(--s4)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;
 color:var(--muted);margin:0 0 var(--s3)}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(2.6rem,8vw,5.5rem);line-height:.95;
 letter-spacing:-.03em;margin:0 0 var(--s2);
 background:linear-gradient(180deg,#fff,var(--chrome) 55%,#6f7d9c);
 -webkit-background-clip:text;background-clip:text;color:transparent}
.tag{font-family:var(--serif);font-style:italic;font-size:clamp(1.15rem,2.4vw,1.6rem);
 color:var(--cream);margin:0 0 var(--s3)}
.deck{color:var(--muted);max-width:62ch;margin:0 0 var(--s2);font-size:1.05rem}
.deck strong{color:var(--fg);font-weight:600}
.sect{margin-top:var(--s5);border-top:1px solid var(--line);padding-top:var(--s3)}
.num{font-family:var(--mono);font-size:.72rem;letter-spacing:.2em;color:var(--chrome);margin:0 0 .4rem}
.sect.red .num{color:var(--red)}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.7rem,3.6vw,2.5rem);line-height:1.1;
 margin:0 0 .25rem;letter-spacing:-.015em;text-wrap:balance}
.sub{font-family:var(--mono);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;
 color:var(--muted);margin:0 0 var(--s2)}
.lede{color:var(--fg);max-width:64ch;margin:0 0 var(--s3);font-size:1.05rem}
.lede em{font-family:var(--serif);font-style:italic;color:var(--cream)}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:var(--s2);
 margin-bottom:var(--s3)}
.strip figure{margin:0}
.strip img{width:100%;height:auto;border:1px solid var(--line);border-radius:3px;
 box-shadow:0 16px 40px -20px rgba(0,0,0,.9)}
.strip figcaption{font-family:var(--mono);font-size:.65rem;letter-spacing:.1em;color:var(--muted);
 text-transform:uppercase;margin-top:.5rem}
.obs{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:var(--s2);
 max-width:66ch}
.obs li{border-left:2px solid var(--line);padding-left:1rem;color:var(--muted)}
.sect.red .obs li{border-left-color:var(--red)}
.obs strong{color:var(--fg);font-weight:600}
.obs em{font-family:var(--serif);font-style:italic;color:var(--cream)}
.close{margin-top:var(--s5);border-top:1px solid var(--line);padding-top:var(--s3)}
.close p{color:var(--muted);max-width:66ch}
.close strong{color:var(--fg)}
footer{margin-top:var(--s4);color:var(--muted);font-size:.82rem;font-family:var(--mono);
 line-height:1.7}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def src(n):
    if MODE == "inline":
        return "data:image/jpeg;base64," + b64(os.path.join(WEB, n + ".jpg"))
    return "posters/" + n + ".jpg"


ALT = {
    "original": "1984-style film poster: a woman's face with neural ports at the temple floats above a night city skyline, a man in a blue jacket in silhouette below, chrome title reading Used Memory.",
    "rerelease": "Grindhouse re-release poster on aged cream stock: a young man runs down a wet red-lit street, title Used Memory in heavy red type.",
    "cast": "Four production portraits in a two-by-two grid against grey seamless: a gaunt man in a torn work jacket, a woman in a leather apron with a magnifier headband, a grinning older man in a suit with an origami crane, and a woman with electrodes at her temple.",
}


def build():
    out = []
    for s in SECTIONS:
        strip = "".join(
            '<figure><img src="%s" width="%d" height="%d" loading="lazy" decoding="async" '
            'alt="%s"><figcaption>Pass %d</figcaption></figure>'
            % (src("%s-%d" % (s["key"], i)), MAN["%s-%d" % (s["key"], i)][0],
               MAN["%s-%d" % (s["key"], i)][1], ALT[s["key"]], i)
            for i in range(1, 5))
        obs = "".join("<li>%s</li>" % o for o in s["obs"])
        out.append("""
  <section class="sect %(cls)s">
    <p class="num">%(n)s</p>
    <h2>%(title)s</h2>
    <p class="sub">%(sub)s</p>
    <p class="lede">%(lede)s</p>
    <div class="strip">%(strip)s</div>
    <ul class="obs">%(obs)s</ul>
  </section>""" % dict(cls=s["cls"], n=s["n"], title=s["title"], sub=s["sub"],
                       lede=s["lede"], strip=strip, obs=obs))

    return ("""<title>Used Memory — a film that does not exist</title>
<style>__CSS__</style>
<div class="page">
  <header>
    <p class="eyebrow">Campaign study &middot; 12 sheets &middot; three treatments</p>
    <h1>Used Memory</h1>
    <p class="tag">&ldquo;Every memory has its price.&rdquo;</p>
    <p class="deck">A film that does not exist, given a complete distribution history. Not one
      poster &mdash; <strong>a prestige 1984 theatrical campaign, a cheaper re-cut re-release,
      and a cast sheet</strong>, each worked through four passes.</p>
    <p class="deck">The interesting artefact is not any single sheet. It is that the two campaigns
      sell <em>opposite films</em> from the same footage, which is exactly what really happened to
      a certain kind of science-fiction picture between its premiere and its second run.</p>
  </header>
%(sections)s
  <section class="close">
    <p><strong>Why this one is different.</strong> Everything else in this collection needed a
      belt label &mdash; a note on what was claimed versus what could be checked. This needs
      none. It invents a studio, a distributor, a director, a cast and a running time, and every
      one of those inventions is signposted by the form itself. A film poster for a film that
      does not exist is not a false claim; it is the oldest honest fiction there is.</p>
    <p>No real marks appear on any sheet. Parallax Pictures and Coronet Releasing are invented,
      as are all cast and crew names. The only genuine trademark anywhere is the generator's own
      watermark.</p>
  </section>
  <footer>
    Twelve images generated with Grok (xAI), 768&times;1152. Grouped and sequenced here; the set
    arrived unlabelled.<br>
    All rights reserved. TerAustralis Incognita &mdash; ABN 70 741 068 059.
  </footer>
</div>""" % dict(sections="".join(out))).replace("__CSS__", CSS.replace("__FONTS__", FONTS))


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
        out = os.path.join(HERE, "um-linked.html")
    else:
        out = os.path.join(HERE, "used-memory.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.0f KB" % (out, MODE, os.path.getsize(out) / 1024))
