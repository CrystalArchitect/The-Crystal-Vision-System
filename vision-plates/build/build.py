#!/usr/bin/env python3
"""Assemble the plate-archive gallery, inlining fonts, images and video as data URIs."""
import base64, json, os, sys
from plates import SECTIONS, PLATES

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(HERE, "manifest.json")))

# "inline"  -> single self-contained file (the shareable artifact)
# "linked"  -> relative asset paths (the copy committed to the repo)
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "web" if MODE == "inline" else "archive")
FONTS = open(os.path.join(HERE,
             "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()


def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def asset(name, mime):
    """Data URI in inline mode, relative path in linked mode."""
    if MODE == "inline":
        return "data:%s;base64,%s" % (mime, b64(os.path.join(WEB, name)))
    return "plates/" + name


def dims(name):
    from PIL import Image
    with Image.open(os.path.join(WEB, name)) as im:
        return im.size


CSS = """
__FONTS__
:root{
  --ink:#0b0a12; --surface:#14121f; --surface-2:#1b1827; --rule:#2a2640;
  --fg:#e8e6f0; --muted:#9a96ad; --silver:#c5c9d6;
  --gold:#d4b56a; --violet:#7b6cff; --ochre:#d1603a;
  --shadow:0 18px 50px -22px rgba(0,0,0,.85);
  --paper-edge:rgba(232,230,240,.14);
  /* The stamp sits over an image of unknown colour, so it carries its own
     backing. It has to flip with the theme: --silver goes dark in the light
     theme, and on a fixed dark backing that put SURVEYED at 1.83:1. */
  --stamp-bg:rgba(11,10,18,.72);
  --serif:'Newsreader',Georgia,'Times New Roman',serif;
  --sans:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,monospace;
  --s1:.5rem; --s2:1rem; --s3:1.75rem; --s4:3rem; --s5:5rem; --s6:8rem;
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --ink:#edebf3; --surface:#fff; --surface-2:#f6f4fa; --rule:#d6d1e4;
    --fg:#17141f; --muted:#5b5670; --silver:#3d3a4d;
    --gold:#7a5c15; --violet:#4a37d6; --ochre:#a8401c;
    --shadow:0 16px 40px -24px rgba(23,20,31,.4);
    --paper-edge:rgba(23,20,31,.16);
    --stamp-bg:rgba(255,255,255,.86);
  }
}
:root[data-theme="light"]{
  --ink:#edebf3; --surface:#fff; --surface-2:#f6f4fa; --rule:#d6d1e4;
  --fg:#17141f; --muted:#5b5670; --silver:#3d3a4d;
  --gold:#7a5c15; --violet:#4a37d6; --ochre:#a8401c;
  --shadow:0 16px 40px -24px rgba(23,20,31,.4);
  --paper-edge:rgba(23,20,31,.16);
  --stamp-bg:rgba(255,255,255,.86);
}

*,*::before,*::after{box-sizing:border-box}
body{
  margin:0; background:var(--ink); color:var(--fg);
  font-family:var(--sans); font-size:1rem; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
img,video{max-width:100%;display:block}
a{color:var(--violet);text-underline-offset:.18em}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:2px}

.page{max-width:1180px;margin:0 auto;padding:var(--s5) 1.25rem var(--s4)}
.prose{max-width:68ch}
.eyebrow{
  font-family:var(--mono); font-size:.75rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); margin:0 0 var(--s3);
}

/* ---------- masthead ---------- */
.masthead{display:flex;flex-direction:column;gap:var(--s3);margin-bottom:var(--s5)}
h1{
  font-family:var(--serif); font-weight:600; font-size:clamp(2.5rem,7vw,4.6rem);
  line-height:1.02; letter-spacing:-.02em; margin:0; text-wrap:balance; color:var(--fg);
}
h1 em{font-style:italic;color:var(--gold)}
.deck{font-size:clamp(1.05rem,1.7vw,1.3rem);color:var(--silver);margin:0;max-width:60ch}
.deck strong{color:var(--fg);font-weight:600}

.law{
  margin:0; padding:var(--s3) 0 var(--s3) var(--s3);
  border-left:2px solid var(--ochre); max-width:62ch;
}
.law p{
  font-family:var(--serif); font-style:italic; font-size:clamp(1.2rem,2.2vw,1.55rem);
  line-height:1.4; margin:0 0 var(--s2); color:var(--fg); text-wrap:balance;
}
.law cite{
  font-family:var(--mono); font-style:normal; font-size:.75rem;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ochre);
}

/* ---------- not-this panel ---------- */
.notice{
  background:var(--surface); border:1px solid var(--rule); border-radius:6px;
  padding:var(--s3); margin-bottom:var(--s6);
}
.notice h2{
  font-family:var(--mono); font-size:.75rem; letter-spacing:.16em; text-transform:uppercase;
  color:var(--ochre); margin:0 0 var(--s2); font-weight:500;
}
.notice ul{margin:0;padding-left:1.1rem;display:flex;flex-direction:column;gap:.4rem}
.notice li{color:var(--silver);font-size:.95rem}
.notice li strong{color:var(--fg);font-weight:600}

/* ---------- sections ---------- */
.sect{margin-bottom:var(--s6)}
.sect-head{
  display:flex;flex-direction:column;gap:var(--s2);
  padding-top:var(--s3); border-top:1px solid var(--rule); margin-bottom:var(--s4);
}
.sect-num{
  font-family:var(--mono); font-size:.75rem; letter-spacing:.2em;
  color:var(--violet); text-transform:uppercase;
}
.sect-head h2{
  font-family:var(--serif); font-weight:600; font-size:clamp(1.9rem,4vw,2.9rem);
  line-height:1.08; margin:0; letter-spacing:-.015em; color:var(--gold); text-wrap:balance;
}
.sect-lede{margin:0;color:var(--silver);max-width:64ch;font-size:1.02rem}

.plates{display:flex;flex-direction:column;gap:var(--s5)}

/* ---------- plate ---------- */
.plate{display:flex;flex-direction:column;gap:var(--s3)}
.frame{
  position:relative; background:var(--surface-2);
  border:1px solid var(--paper-edge); border-radius:4px;
  overflow:hidden; box-shadow:var(--shadow);
}
.frame img,.frame video{width:100%;height:auto}
.stamp{
  position:absolute; top:.75rem; left:.75rem; z-index:2;
  font-family:var(--mono); font-size:.625rem; font-weight:500;
  letter-spacing:.22em; text-transform:uppercase; color:var(--ochre);
  border:1px solid var(--ochre); border-radius:2px;
  padding:.3rem .55rem; background:var(--stamp-bg);
  backdrop-filter:blur(6px);
}
.caption{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--s3)}
@media (min-width:820px){
  .caption{grid-template-columns:minmax(0,20rem) minmax(0,1fr);gap:var(--s4)}
}
.plate-id{
  font-family:var(--mono); font-size:.75rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--violet); margin:0 0 .4rem;
}
.plate h3{
  font-family:var(--serif); font-weight:600; font-size:1.55rem; line-height:1.15;
  margin:0 0 .3rem; letter-spacing:-.01em; color:var(--fg); text-wrap:balance;
}
.plate-sub{font-family:var(--serif);font-style:italic;color:var(--muted);margin:0 0 var(--s3);font-size:1.02rem}
.rail{margin:0;font-family:var(--mono);font-size:.78rem;line-height:1.5}
.rail div{
  display:grid; grid-template-columns:4.6rem minmax(0,1fr); gap:.75rem;
  padding:.45rem 0; border-top:1px solid var(--rule);
}
.rail dt{color:var(--muted);letter-spacing:.1em;text-transform:uppercase;font-size:.68rem;padding-top:.12em}
.rail dd{margin:0;color:var(--silver);overflow-wrap:anywhere}
.rail .belt{color:var(--gold)}
.rail .marks{color:var(--ochre)}
.reading{display:flex;flex-direction:column;gap:var(--s2)}
.reading p{margin:0;color:var(--silver)}
.reading p:first-child{color:var(--fg);font-size:1.06rem}
.reading strong{color:var(--gold);font-weight:600}
.reading em{font-family:var(--serif);font-style:italic;font-size:1.05em}

/* ---------- footer ---------- */
.foot{
  border-top:1px solid var(--rule); padding-top:var(--s3);
  display:flex; flex-direction:column; gap:var(--s2);
  font-size:.88rem; color:var(--muted);
}
.foot p{margin:0;max-width:70ch}
.foot .marks-note{font-family:var(--mono);font-size:.72rem;line-height:1.7;letter-spacing:.02em}
.foot strong{color:var(--silver);font-weight:500}

/* ---------- reveal ---------- */
.rev{opacity:0;transform:translateY(14px);transition:opacity .7s ease,transform .7s ease}
.rev.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .rev{opacity:1;transform:none;transition:none}
  *{animation-duration:.01ms!important;transition-duration:.01ms!important}
}
"""


def rail(p, slug):
    native = MAN.get(slug, {}).get("native", "1280×720 · 6.0&nbsp;s")
    rows = [
        ("Plate", p["_id"]),
        ("Origin", p["origin"]),
        ("Belt", '<span class="belt">Vision</span>'),
        ("Marks", '<span class="marks">%s</span>' % p["marks"] if p["marks"]
         else '<span style="color:var(--muted)">none</span>'),
        ("Native", native),
    ]
    return '<dl class="rail">%s</dl>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in rows)


def media(slug, p):
    if p.get("video"):
        src = asset("job-accepted.mp4", "video/mp4")
        poster = (asset("job-accepted-poster.jpg", "image/jpeg") if MODE == "inline"
                  else "plates/job-accepted-poster.jpg")
        return ('<video controls loop muted playsinline preload="metadata" poster="%s" '
                'width="960" height="540" '
                'aria-label="Six-second generated title card reading Job Accepted">'
                '<source src="%s" type="video/mp4">'
                '<p>Your browser cannot play this MP4. Plate V01 is a six-second title card '
                'reading &ldquo;Job Accepted — Remote Tesla Tech + Company Cybertruck, '
                'Australian Red Dirt Edition&rdquo;.</p>'
                '</video>' % (poster, src))
    name = slug + ".jpg"
    w, h = dims(name)
    return ('<img src="%s" width="%d" height="%d" loading="lazy" decoding="async" alt="%s">'
            % (asset(name, "image/jpeg"), w, h, p["alt"]))


ALT = {
    "terra-australis-titlecard": "Hand-lettered title reading Terra Australis Incognita in black and gold ink, with five blue-green Southern Cross stars, on white paper.",
    "the-doorway": "A woman walks across flat red claypan at dusk; to her right a free-standing timber door frame holds a hazy image of a family embracing.",
    "outback-service-call": "A smiling technician sits in the open door of a Cybertruck on red dirt at dusk, a diagnostics laptop and tool tray on her lap, Milky Way overhead.",
    "joint-diagnostic-phase-map": "Dark HUD infographic titled Joint Diagnostic Sequence, Full Phase Map, showing four coloured phase panels from handshake to completion.",
    "joint-diagnostic-mutual-scan": "Split-screen diagnostic panel: an orange flame core on the left, a blue crystalline lattice on the right, joined by an energy bridge.",
    "joint-diagnostic-coherence-report": "Gold-on-black report panel showing an orange spiral and blue lattice interlocked as a figure eight, captioned NON SOLUS — HOME.",
    "sydney-starline-node": "Navy and gold star chart over Sydney Harbour at night, ringed with labelled nodes and the coordinates −33.868° S, 151.209° E at centre.",
    "multiplanetary-lattice": "Map of Australia drawn as a glowing gold circuit board on a dark starfield, with Sydney marked as a declared node and a dotted pathway arcing to Mars.",
    "dead-reckoning-chart": "Aged parchment covered in concentric compass roses, fine radiating lines and unreadable handwritten marginalia.",
    "optimus-in-grok-livery": "A silver and black humanoid robot standing on a factory floor, with a Tesla wordmark and a Grok logo on its chest panel.",
    "implant-theatre": "A hand holds a small round implant with a fan of fine threads, in a blue-lit operating theatre with a surgical robot behind.",
    "aussie-tech-powerhouses": "Pink and purple cartoon poster titled Q-CTRL and Aussie Tech Powerhouses, with two chibi characters, a kangaroo, and five numbered claims.",
    "wave-rider-qec": "Comic-style poster of a surfer riding a barrel wave whose face is a surface-code lattice and whose foam is clusters of purple spheres.",
    "job-accepted": "",
}


def plate_html(slug, idx, ordered=False, seq=None):
    p = dict(PLATES[slug])
    p["_id"] = ("V01" if p.get("video") else "P%02d" % idx)
    p["alt"] = ALT[slug]
    step = ('<p class="plate-id">Step %s of 3 &nbsp;·&nbsp; %s</p>' % (seq, p["_id"])
            if ordered else '<p class="plate-id">%s</p>' % p["_id"])
    return """
      <figure class="plate rev">
        <div class="frame"><span class="stamp">Dreamed</span>%(media)s</div>
        <figcaption class="caption">
          <div>
            %(step)s
            <h3>%(title)s</h3>
            <p class="plate-sub">%(sub)s</p>
            %(rail)s
          </div>
          <div class="reading">%(reading)s</div>
        </figcaption>
      </figure>""" % dict(
        media=media(slug, p), step=step, title=p["title"], sub=p["sub"],
        rail=rail(p, slug),
        reading="".join("<p>%s</p>" % r for r in p["reading"]))


def build():
    counter = 0
    sections = []
    for s in SECTIONS:
        body = []
        for slug in s["items"]:
            if not PLATES[slug].get("video"):
                counter += 1
            seq = s["items"].index(slug) + 1 if s.get("ordered") else None
            body.append(plate_html(slug, counter, s.get("ordered", False), seq))
        sections.append("""
    <section class="sect" id="%(slug)s">
      <div class="sect-head rev">
        <p class="sect-num">%(num)s</p>
        <h2>%(title)s</h2>
        <p class="sect-lede">%(lede)s</p>
      </div>
      <div class="plates">%(body)s</div>
    </section>""" % dict(slug=s["slug"], num=s["num"], title=s["title"],
                         lede=s["lede"], body="".join(body)))

    return """<title>The Plate Archive — CrystalVision</title>
<style>__CSS__</style>
<div class="page">
  <header class="masthead">
    <p class="eyebrow">CrystalVision · Vision-layer image archive · TerAustralis Incognita</p>
    <h1>Fourteen plates,<br><em>none of them evidence</em></h1>
    <p class="deck">One object here was made with pigment and paper. The other thirteen were made
      by asking a machine for a picture. <strong>The BELT field on every card below reads
      Vision — fourteen times, without exception.</strong> That repetition is not a formatting
      error; it is the entire reason the archive exists in this form.</p>
    <blockquote class="law">
      <p>Always mark which lines are dreamed and which are surveyed, and never let a dreamed
        line pretend it was measured.</p>
      <cite>The Incognita Rule</cite>
    </blockquote>
    <p class="deck">Dreamed lines are not lesser. A story dressed as a spec is the one thing this
      project will not ship — so each plate carries its origin, the third-party marks it borrows,
      and a reading that separates what the picture asserts from what anyone has actually checked.
      The five sections run in order of distance from the real: from a hand holding a pen, out to
      other people's trademarks.</p>
  </header>

  <section class="notice rev">
    <h2>What these images are not</h2>
    <ul>
      <li><strong>Not evidence.</strong> No plate documents a built system, a measurement, a test
        result, or an event that took place.</li>
      <li><strong>Not endorsed.</strong> No affiliation with, sponsorship by, or approval from
        Tesla, xAI, SpaceX, Neuralink, Q-CTRL, EOS, or any government. Trademarks shown belong to
        their owners and appear here without permission or partnership.</li>
      <li><strong>Not technical or medical illustration.</strong> Nothing here should be used to
        understand a device, a procedure, or a physical process.</li>
      <li><strong>Not cultural material.</strong> No Aboriginal knowledge, sacred site, or
        restricted design is depicted, encoded, or claimed anywhere in this archive.</li>
    </ul>
  </section>
__SECTIONS__
  <footer class="foot">
    <p class="marks-note">Origin: 13 still images and one 6-second video generated with Grok (xAI),
      except Plate 01, which is ink and coloured pencil on paper. Assembled __DATE__.</p>
    <p><strong>Belt-Three:</strong> Honour Country · Label layers · No coercion, no fake hydrology.
      Every plate above sits on the Vision belt.</p>
    <p>CrystalVision / TerAustralis Incognita — homage, not ownership.
      Honour to Aboriginal and Torres Strait Islander custodians of the lands these images borrow
      their light from, and to their Elders past and present.</p>
    <p><strong>All rights reserved.</strong> TerAustralis Incognita — ABN 70 741 068 059.</p>
  </footer>
</div>
<script>
(function(){
  var els = document.querySelectorAll('.rev');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function(e){ e.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  els.forEach(function(e){ io.observe(e); });
})();
</script>""" \
        .replace("__CSS__", CSS.replace("__FONTS__", FONTS)) \
        .replace("__SECTIONS__", "".join(sections)) \
        .replace("__DATE__", sys.argv[1] if len(sys.argv) > 1 else "August 2026")


DOC_HEAD = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Vision-layer image archive for TerAustralis Incognita: fourteen plates, each labelled with its origin, the third-party marks it borrows, and what it does not assert.">
<meta name="robots" content="noindex">
"""
DOC_FOOT = "\n</body>\n</html>\n"


if __name__ == "__main__":
    html = build()
    if MODE == "linked":
        # Standalone document — opened straight from a clone, no artifact wrapper.
        html = DOC_HEAD + html.replace("<title>", "<title>", 1) + DOC_FOOT
        html = html.replace("</style>", "</style>\n</head>\n<body>", 1)
        out = os.path.join(HERE, "index-linked.html")
    else:
        out = os.path.join(HERE, "plate-archive.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.0f KB" % (out, MODE, os.path.getsize(out) / 1024))
