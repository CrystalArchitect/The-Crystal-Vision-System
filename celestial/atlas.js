/**
 * Celestial Overlay — the data shape.
 *
 * Three layers under one navigable atlas: tonal relationships, stellar
 * positions, and the correspondence a person draws between them. The
 * Overlay sits on top of Starlines rather than competing with them —
 * Starlines remain the connecting paths in the bus, and this is a stellar
 * projection laid over that idea, not a second meaning for the word.
 *
 * The whole point of the shape is that the Incognita Rule is *structural*
 * here rather than remembered. A dreamed line may be drawn; it may not be
 * drawn in the same ink as a surveyed one. So an entry cannot exist without
 * declaring its belt, a star cannot exist without saying where its numbers
 * came from, and a correspondence cannot claim to be surveyed at all. Those
 * are throws, not warnings — the same discipline as BusHub.validate
 * rejecting unlabeled speech, applied to a map instead of a message.
 *
 * What that buys: the mode layer below is *computed*, so it can be checked
 * against music theory rather than trusted. The sky layer is *surveyed*, a
 * committed extract of the Yale Bright Star Catalogue in stars.js, where every
 * coordinate carries its catalogue and epoch — it stood deliberately empty
 * while none was reachable, because a position typed from memory would be the
 * exact failure this project is named for. The correspondence layer is
 * *dreamed*, offered as a personal atlas entry a person can walk, revise, or
 * set down — and revising one now keeps the hearing it replaced.
 *
 * No dependencies, no build step — the same as the rest of this shell.
 */

/** The two kinds of line, and they are not interchangeable. */
export const BELT = Object.freeze({
  /** Checkable against the world: arithmetic, a catalogue, a running test. */
  SURVEYED: 'surveyed',
  /** Designed, imagined, or offered. Real, and never asserted as measured. */
  DREAMED: 'dreamed',
});

const SEMITONES = 12;

/**
 * The major scale, as intervals in semitones from its tonic.
 * Everything else in the tonal layer is derived from this by rotation, so
 * the seven modes are computed rather than copied — a typo in a remembered
 * list would otherwise be indistinguishable from music theory.
 */
const IONIAN = Object.freeze([0, 2, 4, 5, 7, 9, 11]);

/** In the order they appear as rotations of the major scale. */
const MODE_NAMES = Object.freeze([
  'Ionian', 'Dorian', 'Phrygian', 'Lydian',
  'Mixolydian', 'Aeolian', 'Locrian',
]);

/**
 * Rotate the major scale to its nth degree and re-seat it on zero.
 * Rotating is what a mode *is*; this is the definition, not a lookup.
 */
function rotate(degree) {
  const from = IONIAN[degree];
  return Array.from({ length: IONIAN.length }, (_, i) => {
    const note = IONIAN[(degree + i) % IONIAN.length];
    return (note - from + SEMITONES) % SEMITONES;
  });
}

/**
 * Brightness, in the sense the wheel uses: how many scale degrees sit higher
 * than they do in Ionian. Lydian has one raised degree and is the brightest;
 * Locrian has five lowered and is the darkest. Derived, so the ordering of
 * the wheel is a consequence of the intervals rather than an aesthetic
 * decision someone made and nobody can check.
 */
function brightness(intervals) {
  return intervals.reduce((sum, note, i) => sum + Math.sign(note - IONIAN[i]), 0);
}

/**
 * Whether a perfect fifth stands above the tonic.
 *
 * This is the surveyed fact under the intuition that Locrian is the unstable
 * edge — it is the only diatonic mode whose fifth is diminished, so its
 * tonic triad will not hold still. The edge of the chart is a real property
 * of the intervals, not a mood assigned to it.
 */
function hasPerfectFifth(intervals) {
  return intervals.includes(7);
}

/** The seven diatonic modes, computed. */
export const MODES = Object.freeze(MODE_NAMES.map((name, degree) => {
  const intervals = rotate(degree);
  return Object.freeze({
    belt: BELT.SURVEYED,
    name,
    degree,
    intervals: Object.freeze(intervals),
    brightness: brightness(intervals),
    stable: hasPerfectFifth(intervals),
  });
}));

/** Brightest first: Lydian → Locrian. The wheel's own order. */
export const WHEEL = Object.freeze(
  [...MODES].sort((a, b) => b.brightness - a.brightness));

/**
 * A star, as this atlas will hold one.
 *
 * `source` is required and unforgiving on purpose. Star positions are
 * surveyed or they are nothing, and the way they stop being surveyed is
 * somebody typing a plausible number. Naming the catalogue and the epoch is
 * the difference between a measurement and a recollection.
 */
export function star({ id, name, raHours, decDegrees, magnitude, source }) {
  if (!id || !name) throw new Error('a star needs an id and a name');
  if (!source) {
    throw new Error(
      `star "${name}" has no source — give the catalogue and epoch it came ` +
      `from (e.g. "Hipparcos HIP 60718, J2000"). A position without a ` +
      `provenance is a dreamed line wearing a surveyed coat.`);
  }
  if (!Number.isFinite(raHours) || raHours < 0 || raHours >= 24) {
    throw new Error(`star "${name}": right ascension must be 0–24 hours`);
  }
  if (!Number.isFinite(decDegrees) || decDegrees < -90 || decDegrees > 90) {
    throw new Error(`star "${name}": declination must be -90–90 degrees`);
  }
  return Object.freeze({
    belt: BELT.SURVEYED, id, name, raHours, decDegrees,
    magnitude: Number.isFinite(magnitude) ? magnitude : null,
    source,
  });
}

/**
 * The sky layer lives in `stars.js`, not here.
 *
 * This file held `STARS = []` for as long as no catalogue was reachable, with
 * a comment saying to delete it when that stopped being true. It has stopped
 * being true, so the comment is gone and the stars are real — a committed
 * extract of the Yale Bright Star Catalogue, each entry carrying its epoch.
 *
 * They live next door because `star()` is the gate they pass through, and a
 * gate should not import the things it admits.
 */

/**
 * A correspondence: this mode, felt as that region of sky.
 *
 * Always dreamed. The function refuses any other belt rather than accepting
 * a parameter and trusting the caller, because this is the precise join
 * where a personal atlas could start reading as an astronomical claim. The
 * modes underneath are surveyed and the stars will be; the line drawn
 * between them is somebody's, and stays marked as somebody's.
 */
export function correspondence({ mode, region, colour, note, belt = BELT.DREAMED }) {
  if (belt !== BELT.DREAMED) {
    throw new Error(
      `a mode-to-sky correspondence is a dreamed line and cannot be filed ` +
      `as ${belt}. The modes are surveyed and the stars are surveyed; that ` +
      `they answer to each other is offered, not measured.`);
  }
  if (!MODES.some((m) => m.name === mode)) {
    throw new Error(`"${mode}" is not one of the seven diatonic modes`);
  }
  if (!region) throw new Error('a correspondence needs a region of sky');
  return Object.freeze({
    belt: BELT.DREAMED, mode, region,
    colour: colour ?? '', note: note ?? '',
  });
}

/**
 * How much of a work sits in a territory.
 *
 * Not a number. The readings this holds distinguish where a work lives from
 * where it passes through, and flattening that to a percentage would invent
 * precision nobody measured.
 */
export const DWELL = Object.freeze({
  /** The song's climate. Where it returns to. */
  HOME: 'home',
  /** Genuinely visited, and not the centre. */
  THROUGH: 'through',
  /** Touched briefly — a flash, a lift, one bar. */
  GLANCED: 'glanced',
});

/**
 * The three things the readings kept saying about paths, in a closed
 * vocabulary the wheel can draw.
 *
 * Added because two collisions had accumulated: five readings, three distinct
 * placements, with the distinguishing detail living entirely in the `paths`
 * prose. Every one of these axes was already being written by hand — "short,
 * urgent loops... they do not travel far" against "long, patient arcs
 * stretching across the circle". Nothing here is invented; it is the prose
 * that already existed, given somewhere to live where a drawing can reach it.
 *
 * `motion` is optional, and that is deliberate. Making it required would
 * force every future reading through a vocabulary chosen after five examples,
 * which is too few to legislate from. A reading without it is still a
 * reading; it simply carries less that can be drawn.
 */
export const MOTION = Object.freeze({
  /** How far the paths travel from the centre. */
  REACH: Object.freeze({ NEAR: 'near', FAR: 'far' }),
  /** The tempo of the travelling. */
  PACE: Object.freeze({ URGENT: 'urgent', STEADY: 'steady' }),
  /**
   * What the paths do.
   *
   * `departs` leaves the centre and does not come back; `returns` comes home
   * to it; `shuttles` runs between two territories with the centre
   * incidental; `radiates` climbs *to* the centre and then goes out from it,
   * making the centre a waypoint rather than an origin or a destination.
   *
   * `radiates` was added later than the other three and deliberately late.
   * The first reading it fitted — "This Is Me" — was filed with **no
   * motion at all** rather than forced into `departs`, on the grounds that
   * adding a value on one example is legislating from a single case. A
   * second reading then arrived with the same shape ("Firework": start low,
   * climb to the centre, explode outward), which is the evidence the first
   * one deliberately did not provide. Two independent examples, from
   * different works, described in different words.
   *
   * Recorded because the restraint is the point: the vocabulary grew when
   * the readings asked it to, not when the first awkward case appeared.
   */
  SHAPE: Object.freeze({
    DEPARTS: 'departs', RETURNS: 'returns',
    SHUTTLES: 'shuttles', RADIATES: 'radiates',
  }),
});

function checkMotion(title, motion) {
  if (motion === undefined) return undefined;
  const fields = [['reach', MOTION.REACH], ['pace', MOTION.PACE], ['shape', MOTION.SHAPE]];
  for (const [field, allowed] of fields) {
    if (!Object.values(allowed).includes(motion[field])) {
      throw new Error(
        `"${title}" gives motion.${field} as ${JSON.stringify(motion[field])} — ` +
        `use ${Object.values(allowed).join(', ')}. A half-filled motion is ` +
        `worse than none: it would be counted as a distinction that was ` +
        `never actually drawn.`);
    }
  }
  return Object.freeze({ ...motion });
}

/**
 * A work read onto the wheel: which territories it lives in, which it
 * refuses, and the shape of the paths between them.
 *
 * This exists because the single mode-to-region correspondence above turned
 * out to be too thin for the readings people actually write. Three came in
 * at once and none of them fitted: each named several territories at
 * different depths, each said which territories the work *would not* enter,
 * and each described the paths as having a character — long straight lines
 * to the horizon, or short urgent loops that never leave the centre.
 *
 * `refuses` is the field worth defending. "The song refuses the night
 * country" is a reading, not an absence, and a shape that could only record
 * presence would silently discard the half of the observation that carries
 * the meaning. An empty `refuses` and a deliberate one look identical
 * afterwards unless the difference is stored.
 *
 * Dreamed, all of it, and not negotiable — the modes underneath are
 * arithmetic and the sky will be a catalogue, but that a song lives in
 * Mixolydian is somebody's ear, offered.
 *
 * Lyrics are deliberately not a field. A reading may quote a line in
 * conversation; a repository that stored song text would be doing something
 * else, and the mapping is the part that belongs to whoever made it.
 */
export function reading({ title, artist, centre, territories = [], refuses = [],
                          paths = '', motion, sky = '', asOf, belt = BELT.DREAMED }) {
  if (belt !== BELT.DREAMED) {
    throw new Error(
      `a reading of a work is a dreamed line and cannot be filed as ${belt}.`);
  }
  if (!title || !artist) throw new Error('a reading names the work and who made it');
  if (!territories.length) {
    throw new Error(`"${title}" names no territory — a reading that places a ` +
                    `work nowhere is not yet a reading`);
  }

  const named = new Set();
  for (const t of territories) {
    if (!MODES.some((m) => m.name === t.mode)) {
      throw new Error(`"${t.mode}" is not one of the seven diatonic modes`);
    }
    if (!Object.values(DWELL).includes(t.dwell)) {
      throw new Error(
        `"${title}" places ${t.mode} without saying how deeply — use ` +
        `${Object.values(DWELL).join(', ')}`);
    }
    if (named.has(t.mode)) {
      throw new Error(`"${title}" names ${t.mode} twice`);
    }
    named.add(t.mode);
  }
  for (const mode of refuses) {
    if (!MODES.some((m) => m.name === mode)) {
      throw new Error(`"${mode}" is not one of the seven diatonic modes`);
    }
    if (named.has(mode)) {
      throw new Error(
        `"${title}" both enters and refuses ${mode} — one of the two is wrong`);
    }
  }

  return Object.freeze({
    belt: BELT.DREAMED, title, artist, centre: centre ?? '',
    territories: Object.freeze(territories.map((t) => Object.freeze({ ...t }))),
    refuses: Object.freeze([...refuses]),
    paths, motion: checkMotion(title, motion), sky,
    asOf: asOf ?? null,
  });
}

/**
 * A revised hearing of a work, keeping the earlier one.
 *
 * A reading is how somebody hears a song *on a day*. Hear it again in ten
 * years and the placement moves — the night country becomes daylight, a
 * refusal softens to a glance. Until now the shape could not hold that:
 * revising a reading meant editing it, and editing it destroyed the hearing
 * it replaced. The atlas remembered only the latest opinion and presented it
 * as the only one there had ever been.
 *
 * So a revision does not overwrite. It carries its predecessor, and `history()`
 * walks the chain back. The old reading stays exactly as it was written,
 * because it was true of the person who wrote it at the time, and a map that
 * quietly replaces the past is doing the thing this project is named against.
 *
 * `asOf` is required on a revision and stays plain data — never generated
 * here. When a person heard something is theirs to state, not this file's to
 * stamp.
 */
export function revise(previous, changes) {
  if (!previous || previous.belt !== BELT.DREAMED) {
    throw new Error('a revision needs the reading it revises');
  }
  if (!changes || !changes.asOf) {
    throw new Error(
      `revising "${previous.title}" needs an asOf date — a rehearing without ` +
      `a date cannot be placed in the sequence it exists to record`);
  }
  const next = reading({
    title: previous.title, artist: previous.artist,
    centre: previous.centre, territories: previous.territories,
    refuses: previous.refuses, paths: previous.paths,
    motion: previous.motion, sky: previous.sky,
    ...changes,
  });
  return Object.freeze({ ...next, supersedes: previous });
}

/**
 * Every hearing of a work, oldest first.
 * The point of keeping the chain is that it can be walked, not merely stored.
 */
export function history(read) {
  const chain = [];
  for (let r = read; r; r = r.supersedes) chain.unshift(r);
  return chain;
}

/**
 * Take a list of readings into the atlas, refusing to hold the same work twice.
 *
 * `reading()` validates one entry and cannot see its siblings, so this is the
 * only place a duplicate can be caught. It matters more than it looks.
 * Readings arrive by being pasted in, and the same one arriving twice is
 * ordinary — it happened, which is why this exists.
 *
 * Without it, a doubled entry is not merely redundant: it is reported as a
 * *finding*. collisions() sees two records placing a work identically and
 * says the vocabulary cannot tell them apart; resolution() counts six
 * readings and three placements. Both are measurements of a mistake, dressed
 * as measurements of the map. An atlas that miscounts itself and presents the
 * miscount as an insight is the exact failure this layer is built against,
 * committed by the machinery meant to prevent it.
 *
 * So it throws rather than de-duplicating quietly. Two copies of one work
 * means somebody lost track of what was already filed, and silently swallowing
 * the second one hides that from them.
 */
export function register(readings) {
  const seen = new Set();
  for (const read of readings) {
    const key = `${read.title} ${read.artist}`.toLowerCase();
    if (seen.has(key)) {
      throw new Error(
        `"${read.title}" by ${read.artist} is already in the atlas. A work ` +
        `held twice is counted twice, and the second copy would be reported ` +
        `as two works the vocabulary cannot separate — a mistake wearing the ` +
        `shape of a finding.`);
    }
    seen.add(key);
  }
  return Object.freeze([...readings]);
}

/**
 * The territories a reading never mentions — neither entered nor refused.
 *
 * Silence is not refusal, and the difference matters when a reading is
 * revisited later: an unmentioned mode is a question nobody has answered,
 * while a refused one is an answer.
 */
export function unspoken(read) {
  const spoken = new Set([...read.territories.map((t) => t.mode), ...read.refuses]);
  return MODES.filter((m) => !spoken.has(m.name)).map((m) => m.name);
}

/**
 * Refuse anything that will not say which kind of line it is.
 *
 * The mirror of BusHub.validate rejecting unlabeled speech. An atlas that
 * silently accepted an unlabeled entry would let the distinction rot from
 * the inside, one convenient omission at a time.
 */
export function validate(entry) {
  if (!entry || typeof entry !== 'object') {
    throw new Error('not an atlas entry');
  }
  if (entry.belt !== BELT.SURVEYED && entry.belt !== BELT.DREAMED) {
    throw new Error(
      `atlas entry has no belt. Every line says whether it was surveyed or ` +
      `dreamed before it is drawn.`);
  }
  return entry;
}

/**
 * What the atlas can presently show, and what it cannot.
 * Reported rather than left for a reader to infer from an empty panel.
 */
export function coverage(stars = []) {
  return {
    modes: MODES.length,
    stars: stars.length,
    unstableModes: MODES.filter((m) => !m.stable).map((m) => m.name),
    skyAwaitingCatalogue: stars.length === 0,
  };
}
