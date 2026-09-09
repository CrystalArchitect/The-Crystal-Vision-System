#!/usr/bin/env python3
"""Assemble Volume II of the plate archive."""
import base64, json, os, sys
import plates2
from plates2 import SECTIONS, P, HELD_OUT
from build import CSS as CSS1

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "inline")
WEB = os.path.join(HERE, "web2" if MODE == "inline" else "archive2")
MAN = json.load(open(os.path.join(HERE, "manifest2.json")))
FONTS = open(os.path.join(HERE, "fonts.css" if MODE == "inline" else "fonts-linked.css")).read()
VOL1_URL = "https://claude.ai/code/artifact/ed094b96-1a7e-442e-9ba1-a938c42bc28e"

EXTRA_CSS = """
.backlink{
  font-family:var(--mono); font-size:.78rem; letter-spacing:.04em;
  padding:.7rem 0; border-top:1px solid var(--rule); border-bottom:1px solid var(--rule);
  color:var(--muted);
}
.backlink a{color:var(--gold)}
.flag{
  border:1px solid var(--ochre); border-left-width:3px; border-radius:4px;
  background:var(--surface); padding:var(--s3); margin-top:var(--s2); max-width:68ch;
}
.flag h3{
  font-family:var(--mono); font-size:.7rem; letter-spacing:.18em; text-transform:uppercase;
  color:var(--ochre); margin:0 0 .6rem; font-weight:500;
}
.flag p{margin:0;color:var(--silver);font-size:.95rem}
.heldout{
  background:var(--surface); border:1px solid var(--ochre); border-radius:6px;
  padding:var(--s3); margin:var(--s5) 0 0;
}
.heldout h2{
  font-family:var(--serif); font-size:1.5rem; color:var(--gold); margin:0 0 var(--s2);
  font-weight:600; letter-spacing:-.01em;
}
.heldout p{margin:0 0 var(--s2);color:var(--silver);max-width:68ch}
.heldout ol{margin:var(--s2) 0 0;padding-left:1.2rem;display:flex;flex-direction:column;gap:.55rem}
.heldout li{color:var(--muted);font-family:var(--mono);font-size:.78rem;line-height:1.55}
.tally{
  display:flex;flex-wrap:wrap;gap:var(--s3);margin:0;padding:0;list-style:none;
  font-family:var(--mono);font-size:.75rem;
}
.tally div{display:flex;flex-direction:column;gap:.15rem}
.tally dt{color:var(--muted);letter-spacing:.14em;text-transform:uppercase;font-size:.65rem}
.tally dd{margin:0;color:var(--gold);font-size:1.5rem;font-variant-numeric:tabular-nums}
.tally dd.ok{color:var(--silver)}
"""


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def asset(name):
    if MODE == "inline":
        return "data:image/jpeg;base64," + b64(os.path.join(WEB, name))
    return "plates/" + name


def rail(slug, p, pid):
    rows = [("Plate", pid), ("Origin", p["origin"]), ("Belt", '<span class="belt">Vision</span>')]
    if slug in ("eulers-identity", "gimbardidoo-lsk170-schematic", "gimbardidoo-active-model-2",
                "gimbardidoo-electronic-section", "gimbardidoo-lavictoire-integration"):
        rows[2] = ("Belt", '<span style="color:var(--silver)">Science &mdash; checkable</span>')
    rows += [
        ("Marks", '<span class="marks">%s</span>' % p["marks"] if p["marks"]
         else '<span style="color:var(--muted)">none</span>'),
        ("Native", MAN[slug]["native"]),
    ]
    return '<dl class="rail">%s</dl>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in rows)


def plate_html(slug, pid):
    p = P[slug]
    w, h = MAN[slug]["web"]
    stamp = "Dreamed"
    if slug in ("eulers-identity", "gimbardidoo-lsk170-schematic", "gimbardidoo-active-model-2",
                "gimbardidoo-electronic-section", "gimbardidoo-lavictoire-integration"):
        stamp = "Surveyed"
    alt = "%s — %s. %s" % (p["title"].replace("&mdash;", "—"), p["sub"],
                           p["reading"][0][:180])
    import re
    alt = re.sub(r"<[^>]+>", "", alt).replace("&ldquo;", "“").replace("&rdquo;", "”") \
            .replace("&mdash;", "—").replace("&nbsp;", " ").replace("&percnt;", "%") \
            .replace("&amp;", "&").replace("&middot;", "·").replace("&rsquo;", "’")
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

    held = "".join("<li>%s</li>" % d for _, d in HELD_OUT)

    return ("""<title>The Plate Archive, Volume II — CrystalVision</title>
<style>__CSS__</style>
<div class="page">
  <header class="masthead">
    <p class="eyebrow">CrystalVision · Vision-layer image archive · Volume II</p>
    <h1>Sixty-six plates,<br><em>and five that hold up</em></h1>
    <p class="deck">Volume I could say one thing about all fourteen of its plates: none of them
      were evidence. This volume cannot. <strong>Five plates here survive being checked</strong>
      &mdash; four are a working analogue circuit, one is a proof &mdash; and they are drawn in
      very nearly the same style as six that assert a warp drive and a zero-point reactor.</p>
    <p class="deck">So the sections no longer run by subject. They run by <em>how hard a claim
      each plate makes, and whether it can carry it</em>.</p>
    <blockquote class="law">
      <p>Always mark which lines are dreamed and which are surveyed, and never let a dreamed
        line pretend it was measured.</p>
      <cite>The Incognita Rule</cite>
    </blockquote>
    <dl class="tally">
      <div><dt>Plates</dt><dd>66</dd></div>
      <div><dt>Survive checking</dt><dd class="ok">5</dd></div>
      <div><dt>Held out</dt><dd>4</dd></div>
      <div><dt>Carry others&rsquo; marks</dt><dd>11</dd></div>
    </dl>
    <p class="backlink">Volume I &mdash; fourteen plates, none of them evidence &mdash;
      <a href="%(vol1)s">is here</a>.</p>
  </header>

  <section class="notice rev">
    <h2>What these images are not</h2>
    <ul>
      <li><strong>Not evidence</strong>, except where section II says otherwise. No dashboard
        here reports a running system; no reactor drawing describes a machine.</li>
      <li><strong>Not endorsed.</strong> No affiliation with Tesla, xAI, SpaceX, Neuralink,
        Starlink, E.C. Publications, Lucasfilm, or any government. Marks shown belong to their
        owners and appear without permission.</li>
      <li><strong>Not teaching material.</strong> Section VIII is styled as a class. It is not
        one, and nothing in it should be studied as physics or medicine.</li>
      <li><strong>Not cultural material.</strong> Four plates that pinned real named Aboriginal
        communities and a named Seven Sisters site were held out of this archive entirely; see
        the closing note.</li>
    </ul>
  </section>
%(sections)s
  <section class="heldout rev">
    <h2>Held out of this archive</h2>
    <p>Four plates in the same batch mapped <strong>real, named Aboriginal communities and
      Country</strong> as nodes in the CrystalCore lattice &mdash; among them Parnngurr, Punmu,
      Kalypa (Well&nbsp;23), Pangkapini, Ngaanyatjarra Country, the APY Lands, the Musgrave
      Ranges, and <strong>Cave Hill / Walinynga</strong>, a Seven Sisters rock-art site with
      living custodians.</p>
    <p>They are not catalogued above and they were not committed anywhere. This project&rsquo;s
      own governance holds that no Songline knowledge enters any model, dataset or index without
      Free, Prior and Informed Consent from the relevant custodians, and that the law is a floor
      rather than a ceiling. Plotting living communities as infrastructure in a private fictional
      network is a decision for the author to take with custodians &mdash; not one to make by
      default, and not one an archivist should make quietly on someone else&rsquo;s behalf.</p>
    <ol>%(held)s</ol>
  </section>

  <footer class="foot">
    <p class="marks-note">Origin: 65 images generated with Grok (xAI); one typeset screenshot
      (Plate&nbsp;02). Three plates in section&nbsp;V are photographs of pages printed and held.
      Snapshot taken %(date)s; the source set was still growing when this was assembled.</p>
    <p><strong>Belt-Three:</strong> Honour Country · Label layers · No coercion, no fake
      hydrology. Sixty-one plates above sit on the Vision belt; five sit on Science, and say so.</p>
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
</script>""" % dict(sections="".join(out), held=held, date=date, vol1=VOL1_URL)
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
        out = os.path.join(HERE, "index2-linked.html")
    else:
        out = os.path.join(HERE, "plate-archive-vol2.html")
    open(out, "w").write(html)
    print("wrote %s (%s) — %.2f MB" % (out, MODE, os.path.getsize(out) / 1024 / 1024))
