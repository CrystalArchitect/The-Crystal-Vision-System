/**
 * The sky layer, no longer empty.
 *
 * Twenty-eight stars from the Yale Bright Star Catalogue, 5th edition —
 * equinox J2000, epoch 2000.0 — committed as a fixed extract rather than
 * fetched at runtime. That was a decision, not a convenience: a runtime fetch
 * is a silent network dependency and a moving target, and this project's
 * architecture calls both of those failures. The extract is offline, versioned,
 * diffable, and refreshable by re-running `extract-stars.js` deliberately.
 *
 * Two groups, both chosen for reasons rather than tidiness.
 *
 * `bright-south` is the sky the readings keep describing. Every reading so far
 * places its work "low in the southern sky", so these are the stars a person
 * actually standing in this project's hemisphere would be looking at.
 *
 * `pleiades` is here because the umbrella's `research/seven-sisters/` folder
 * already names **Atlas** and **Pleione** as the parental frame of the cluster
 * — and Atlas is also the word this whole layer is built on. Mercator named
 * the map-book for a celestial cartographer, and the star carrying that name
 * is in the catalogue at HR 1178. That is a coincidence rather than evidence,
 * and it is noted here as a coincidence.
 *
 * Every entry goes through `star()`, which refuses a position with no source.
 * That check is the point of this file existing at all: the catalogue and the
 * epoch travel with each coordinate, so a number here can be argued with.
 */

import { star } from './atlas.js';
import { RAW } from './stars.data.js';

/**
 * Where every position in this file comes from.
 *
 * Named precisely enough to be checked and, if wrong, corrected. "Yale" alone
 * would not be: the catalogue has editions, and the same star carries
 * different numbers in the B1900 and J2000 columns of the same row. The
 * conversion this extract was taken from exposes both; this file uses the
 * J2000 pair, and says so.
 */
export const SOURCE =
  'Yale Bright Star Catalogue, 5th ed. (Hoffleit & Warren), equinox J2000, ' +
  'epoch 2000.0 — via brettonw/YaleBrightStarCatalog bsc5.json (MIT), ' +
  'retrieved 11 August 2026';

/** The extract, each entry validated by the same rule as any other star. */
export const STARS = Object.freeze(RAW.map((s) => Object.freeze({
  ...star({
    id: s.id, name: s.name, raHours: s.raHours,
    decDegrees: s.decDegrees, magnitude: s.magnitude, source: SOURCE,
  }),
  designation: s.designation,
  group: s.group,
})));

/** The stars in one named group. */
export function group(name, stars = STARS) {
  return stars.filter((s) => s.group === name);
}

/**
 * What is in the extract and what is deliberately not.
 *
 * The gap matters more than the contents. Nine thousand and ninety-six stars
 * were available; twenty-eight are here. Anyone reading a drawing made from
 * this file is looking at a chosen subset, and a subset that does not say so
 * reads as a sky.
 */
export function extractNote() {
  return `${STARS.length} stars of the 9,096 in the source catalogue, chosen ` +
         `for two purposes: the brightest visible from southern latitudes, ` +
         `and the Pleiades. This is an extract, not the sky. Absence here ` +
         `means "not selected", never "not there".`;
}
