#!/usr/bin/env python3
"""Assemble Volume III of the plate archive.

Structurally build2.py, with the three things that were hard-coded to Volume II
moved where they belong:

* the SURVEYED slugs now live in `plates3.SURVEYED` instead of being written out
  twice, once in `rail()` and once in `plate_html()`
* the tally counts are derived from the catalogue rather than typed
* the closing block records what was removed from the volume and why, rather
  than Volume II's held-out list

`build2.py` itself is left alone — a fourth volume should copy this file rather
than that one. All three volumes share `build.py`'s CSS, so a change there
regenerates all three galleries; that is how the stamp-contrast fix reached
Volumes I and II.

Run `python3 fonts.py --prefix ../fonts/` first — the import below opens its
output. See build/README.md.
"""
import base64, json, os, sys
from plates3 import SECTIONS, P, SURVEYED
from build import CSS as CSS1
from build2 import EXTRA_CSS

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "web3" if MODE == "inline" else "archive3")
MAN = json.load(open(os.path.join(HERE, "manifest3.json")))
FONTS = open(os.path.join(HERE, "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()
VOL1_URL = "../index.html"
VOL2_URL = "../volume-2/index.html"

# The stamp's illegibility in the light theme is fixed in build.py's shared CSS
# via --stamp-bg, so all three volumes inherit it. It surfaced here, on a
# surveyed plate over a black image — a plate since removed from this volume,
# though the bug it exposed was real and the fix stands.


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def asset(name):
    if MODE == "inline":
        return "data:image/jpeg;base64," + b64(os.path.join(WEB, name))
    return "plates/" + name


def rail(slug, p, pid):
    belt = ('<span style="color:var(--silver)">Science &mdash; checkable</span>'
            if slug in SURVEYED else '<span class="belt">Vision</span>')
    rows = [
        ("Plate", pid),
        ("Origin", p["origin"]),
        ("Belt", belt),
        ("Marks", '<span class="marks">%s</span>' % p["marks"] if p["marks"]
         else '<span style="color:var(--muted)">none</span>'),
        ("Native", MAN[slug]["native"]),
    ]
    return '<dl class="rail">%s</dl>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in rows)


def plate_html(slug, pid):
    import re
    p = P[slug]
    w, h = MAN[slug]["web"]
    stamp = "Surveyed" if slug in SURVEYED else "Dreamed"
    alt = "%s — %s. %s" % (p["title"].replace("&mdash;", "—"), p["sub"], p["reading"][0][:180])
    alt = re.sub(r"<[^>]+>", "", alt).replace("&ldquo;", "“").replace("&rdquo;", "”") \
            .replace("&mdash;", "—").replace("&nbsp;", " ").replace("&percnt;", "%") \
            .replace("&amp;", "&").replace("&middot;", "·").replace("&rsquo;", "’") \
            .replace("&flat;", "♭").replace("&sharp;", "♯").replace("&deg;", "°") \
            .replace("&ndash;", "–")
    return """
      <figure class="plate rev">
        <div class="frame"><span class="stamp"%(sc)s>%(stamp)s</span>
          <img src="%(src)s" width="%(w)d" height="%(h)d" loading="lazy" decoding="async" alt="%(alt)s"></div>
        <figcaption class="caption">
          <div>
            <p class="plate-id">%(pid)s</p>
            <h3>%(title)s</h3>
            <p class="plate-sub">%(sub)s</p>
            %(rail)s
          </div>
          <div class="reading">%(reading)s</div>
        </figcaption>
      </figure>""" % dict(
        src=asset(slug + ".jpg"), w=w, h=h, alt=alt.replace('"', "&quot;"),
        stamp=stamp, sc=' style="color:var(--silver);border-color:var(--silver)"'
        if stamp == "Surveyed" else "",
        pid=pid, title=p["title"], sub=p["sub"], rail=rail(slug, p, pid),
        reading="".join("<p>%s</p>" % r for r in p["reading"]))


def build(date):
    n = 0
    out = []
    for s in SECTIONS:
        body = []
        for slug in s["items"]:
            n += 1
            body.append(plate_html(slug, "P%02d" % n))
        flag = ('<div class="flag"><h3>Flagged against this project&rsquo;s own governance</h3>'
                '<p>%s</p></div>' % s["flag"]) if s.get("flag") else ""
        out.append("""
    <section class="sect" id="%(slug)s">
      <div class="sect-head rev">
        <p class="sect-num">%(num)s</p>
        <h2>%(title)s</h2>
        <p class="sect-lede">%(lede)s</p>
        %(flag)s
      </div>
      <div class="plates">%(body)s</div>
    </section>""" % dict(slug=s["slug"], num=s["num"], title=s["title"], lede=s["lede"],
                         flag=flag, body="".join(body)))

    marked = sum(1 for p in P.values() if p["marks"])

    return ("""<title>The Plate Archive, Volume III — CrystalVision</title>
<style>__CSS__</style>
<div class="page">
  <header class="masthead">
    <p class="eyebrow">CrystalVision · Vision-layer image archive · Volume III</p>
    <h1>Two plates,<br><em>and they are one picture</em></h1>
    <p class="deck">Volume I could say one thing about all fourteen of its plates: none were
      evidence. Volume II found five that were. This volume is very small and makes one point:
      <strong>an illustration, and the same illustration issued as a chart.</strong></p>
    <p class="deck">Nothing in the picture changed between them. What was added was a compass
      rose, a dashed route and four place names &mdash; conventions a reader has been trained
      to take as a promise that someone went and looked. Nothing was measured before they were
      added and nothing was measured after.</p>
    <blockquote class="law">
      <p>Always mark which lines are dreamed and which are surveyed, and never let a dreamed
        line pretend it was measured.</p>
      <cite>The Incognita Rule</cite>
    </blockquote>
    <dl class="tally">
      <div><dt>Plates</dt><dd>%(total)d</dd></div>
      <div><dt>Survive checking</dt><dd class="ok">%(surveyed)d</dd></div>
      <div><dt>Held out</dt><dd>0</dd></div>
      <div><dt>Carry others&rsquo; marks</dt><dd>%(marked)d</dd></div>
    </dl>
    <p class="backlink">Volume I &mdash; fourteen plates, none of them evidence &mdash;
      <a href="%(vol1)s">is here</a>. Volume II &mdash; sixty-six plates, five that hold up
      &mdash; <a href="%(vol2)s">is here</a>.</p>
  </header>

  <section class="notice rev">
    <h2>What these images are not</h2>
    <ul>
      <li><strong>Not evidence.</strong> Neither plate documents a built system, a measurement
        or an event. Both sit on the Vision belt.</li>
      <li><strong>Not a map.</strong> Plate&nbsp;02 carries a compass rose, a route and four
        place names, and is not a map of anywhere. That is the reason it is catalogued.</li>
      <li><strong>Not cultural material.</strong> No Aboriginal knowledge, sacred site or
        restricted design is depicted, encoded or claimed anywhere in this volume.</li>
    </ul>
  </section>
%(sections)s
  <section class="heldout rev">
    <h2>Three plates came out of this volume</h2>
    <p>This volume was drafted at five. Three were removed on 11&nbsp;August&nbsp;2026 once
      their provenance was established: they were <strong>collected from elsewhere rather than
      made for this project</strong> &mdash; among them a diagram of the diatonic system that
      had been checked, found correct, and given the silver <em>Surveyed</em> stamp.</p>
    <p>Being correct is not the same as being ours. A plate archive that catalogues other
      people&rsquo;s work as its own vision layer has already misled its reader in the rail,
      before a word of the reading is reached, and no amount of accuracy further down the page
      repairs that. The images were not committed anywhere.</p>
    <p>Origins for the two that remain were not supplied. Volumes&nbsp;I and&nbsp;II name a
      generator for every plate; these rails read <strong>Origin: not supplied</strong> rather
      than carrying a guess. It is one line per plate in <code>build/plates3.py</code> whenever
      the maker records them.</p>
  </section>

  <footer class="foot">
    <p class="marks-note">Snapshot taken %(date)s. Both plates are the author&rsquo;s own work;
      three drafted plates that were not are recorded above rather than quietly dropped. The
      source set was still growing when this was assembled.</p>
    <p><strong>Belt-Three:</strong> Honour Country · Label layers · No coercion, no fake
      hydrology. Both plates above sit on the Vision belt, as all fourteen of Volume&nbsp;I do.</p>
    <p>CrystalVision / TerAustralis Incognita &mdash; homage, not ownership. Honour to Aboriginal
      and Torres Strait Islander custodians of the lands these images borrow their light from,
      and to their Elders past and present.</p>
    <p><strong>All rights reserved.</strong> TerAustralis Incognita &mdash; ABN 70 741 068 059.</p>
  </footer>
</div>
<script>
(function(){
  var els = document.querySelectorAll('.rev');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function(e){ e.classList.add('in'); }); return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8%% 0px', threshold: 0.05 });
  els.forEach(function(e){ io.observe(e); });
})();
</script>""" % dict(sections="".join(out), date=date, vol1=VOL1_URL, vol2=VOL2_URL,
                    total=len(P), surveyed=len(SURVEYED), marked=marked)
    ).replace("__CSS__", CSS1.replace("__FONTS__", FONTS) + EXTRA_CSS)


DOC_HEAD = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
"""

if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "August 2026"
    html = build(date)
    if MODE == "linked":
        html = DOC_HEAD + html.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n"
        out = os.path.join(HERE, "index3-linked.html")
    else:
        out = os.path.join(HERE, "plate-archive-vol3.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.2f MB" % (out, MODE, os.path.getsize(out) / 1024 / 1024))
