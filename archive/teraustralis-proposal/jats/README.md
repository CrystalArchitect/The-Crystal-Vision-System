# JATS interchange

[`review-pack.xml`](review-pack.xml) is a **JATS 1.3** article wrapping the Review Pack for machine interchange (Crossref-shaped metadata, not a journal).

It is **not**:

- a minted DOI
- an ISSN **for this sitting** (none assigned — do not invent `0000-0000`)
- peer review
- CARE compliance
- a substitute for [review.html](https://proposal.teraustralis.com.au/review.html)

ISSNs that **are** in the XML belong to **cited journals**, verified on the ISSN portal:

- *Data Science Journal* — [1683-1470](https://portal.issn.org/resource/ISSN/1683-1470)
- *Remote Sensing of Environment* — print [0034-4257](https://portal.issn.org/resource/ISSN/0034-4257), online [1879-0704](https://portal.issn.org/resource/ISSN/1879-0704)

A DTD that requires `<issn>` on `<journal-meta>` will still fail. That is correct: this is not a serial. To become one, apply through [ISSN Australia / NLA](https://www.nla.gov.au/collections/what-we-collect/journals), then put the assigned number here.

Canonical page remains the HTML sitting.

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('jats/review-pack.xml'); print('well-formed')"
```
