# vendor/

Third-party libraries the prototypes load directly, kept here rather than
fetched from a CDN at page load.

## d3.v7.min.js

D3 7.9.0, the `dist/d3.min.js` build from the `d3` npm package, unmodified.
Copyright Mike Bostock, ISC licence — https://github.com/d3/d3.

`index-v2-integrated.html` and `index-v3-complete-archive.html` previously
loaded this from `https://d3js.org/d3.v7.min.js` with no Subresource
Integrity attribute, on a URL that tracks the newest 7.x release. That meant
the file could change under the prototype at any time, with nothing to
detect it — and it made a prototype that STATUS.md calls "self-contained"
depend on a live third-party host to render at all.

Vendoring settles both: the bytes are pinned in git where a diff shows any
change, and the prototype now opens offline.
