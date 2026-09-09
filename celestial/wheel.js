/**
 * The wheel, drawn.
 *
 * Seven territories around a centre, in brightness order — Lydian at the top
 * and Locrian at the bottom — with a work's rays laid over them. The order
 * is not a design decision: it comes from the interval arithmetic in
 * atlas.js, so the picture is a view of the data rather than a second,
 * prettier copy of it that can disagree.
 *
 * Three things this drawing refuses to do, all for the same reason.
 *
 * It does not draw stars. The sky layer is empty because no catalogue was
 * reachable, and a scattering of decorative points would be a dreamed line
 * rendered in surveyed ink — the exact failure the project is named for.
 * Where the sky would be, it says the sky is empty.
 *
 * It does not silently omit refused territories. A refusal is a reading, so
 * a refused mode is drawn and marked, not left off. Absence would render a
 * deliberate "the song will not go here" identically to "nobody has said".
 *
 * And it marks the whole picture dreamed, on its face, because a diagram
 * travels further than the file it came from and arrives without context.
 */

import { BELT, MODES, WHEEL, DWELL, unspoken } from './atlas.js';

/**
 * Where each territory sits, as fractions of the drawing.
 *
 * Pure and separate from the SVG so the placement can be checked without a
 * browser: brightest at the top, going clockwise, evenly spaced.
 */
export function wheelGeometry({ radius = 1 } = {}) {
  const step = 360 / WHEEL.length;
  return WHEEL.map((mode, i) => {
    const degrees = -90 + i * step;
    const radians = (degrees * Math.PI) / 180;
    return {
      mode: mode.name,
      brightness: mode.brightness,
      stable: mode.stable,
      degrees: (degrees + 360) % 360,
      x: Math.cos(radians) * radius,
      y: Math.sin(radians) * radius,
    };
  });
}

/** How strongly a ray is drawn, by how deeply the work dwells there. */
const REACH = { [DWELL.HOME]: 1, [DWELL.THROUGH]: 0.68, [DWELL.GLANCED]: 0.36 };

/**
 * A reading as SVG.
 *
 * Returns a string rather than touching the DOM, so it can be rendered in a
 * page, written to a file, or asserted against in a test without a browser.
 */
export function drawReading(read, { size = 520 } = {}) {
  const mid = size / 2;
  const r = size * 0.36;
  const placed = new Map(read.territories.map((t) => [t.mode, t]));
  const refused = new Set(read.refuses);
  const quiet = new Set(unspoken(read));

  const rays = [];
  const marks = [];

  for (const spot of wheelGeometry({ radius: r })) {
    const x = mid + spot.x;
    const y = mid + spot.y;
    const here = placed.get(spot.mode);

    if (here) {
      const reach = REACH[here.dwell];
      // Two strokes, because length alone cannot carry both facts. The ray's
      // length is how deeply the work dwells; the faint line under it says
      // *which* territory that is. Drawn once without the second, a glanced
      // ray was a short grey stub near the centre that pointed nowhere a
      // reader could name — so the picture lost exactly the distinction the
      // data was widened to hold: glanced is not refused, and a mark nobody
      // can attribute is indistinguishable from a smudge.
      rays.push(
        `<line x1="${mid}" y1="${mid}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" ` +
        `class="toward ${here.dwell}" />`);
      rays.push(
        `<line x1="${mid}" y1="${mid}" x2="${(mid + spot.x * reach).toFixed(1)}" ` +
        `y2="${(mid + spot.y * reach).toFixed(1)}" ` +
        `class="ray ${here.dwell}" />`);
    }

    // Refused territories are drawn and struck, never omitted: leaving them
    // out would make "the song will not go here" look like silence.
    const state = here ? here.dwell : refused.has(spot.mode) ? 'refused'
      : quiet.has(spot.mode) ? 'unspoken' : 'unspoken';
    marks.push(
      `<g class="territory ${state}" transform="translate(${x.toFixed(1)},${y.toFixed(1)})">` +
      `<circle r="${here ? 7 : 4.5}" />` +
      (refused.has(spot.mode)
        ? '<path class="struck" d="M-6,-6 L6,6 M6,-6 L-6,6" />' : '') +
      `<text y="-14">${spot.mode}</text>` +
      (spot.stable ? '' : '<text class="edge" y="24">no perfect fifth</text>') +
      '</g>');
  }

  return `<svg viewBox="0 0 ${size} ${size}" class="wheel" role="img"
     aria-label="${read.title} placed on the mode wheel — a dreamed line">
  <title>${read.title} — ${read.artist}</title>
  <desc>A dreamed reading. Territories are the seven diatonic modes in
    brightness order; rays show where the work dwells. No star positions are
    drawn: the sky layer holds none.</desc>
  <circle class="rim" cx="${mid}" cy="${mid}" r="${r}" />
  ${rays.join('\n  ')}
  <circle class="centre" cx="${mid}" cy="${mid}" r="6" />
  ${marks.join('\n  ')}
  <text class="belt" x="${mid}" y="${size - 12}">dreamed line — not an astronomical chart</text>
</svg>`;
}

/**
 * What the sky panel says while the catalogue is missing.
 * A sentence rather than an empty box, so the gap reads as a known one.
 */
export function skyNotice(stars) {
  return stars.length === 0
    ? 'The sky layer holds no stars yet. None are drawn rather than drawn ' +
      'from memory — a position without a catalogue behind it would be a ' +
      'dreamed line wearing a surveyed coat.'
    : `${stars.length} stars, each carrying the catalogue it came from.`;
}

/** The belt this drawing is on, stated for anything that asks. */
export const DRAWING_BELT = BELT.DREAMED;

/** Exported for the page: every mode, in the order the wheel draws them. */
export const WHEEL_ORDER = Object.freeze(MODES.map((m) => m.name));
