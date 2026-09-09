/**
 * The Celestial Overlay's data shape, checked.
 *
 * Two things are being tested and they are not the same thing. The tonal
 * layer is arithmetic, so it can simply be right or wrong — these assert it
 * against music theory rather than against what the file happens to say.
 *
 * The rest asserts that the shape *refuses* things. That matters more. A map
 * of dream territories laid over real stars is exactly the kind of artefact
 * that drifts into being read as a star chart, and it drifts one unlabeled
 * entry at a time. So the throws are the feature, and these are the tests
 * that will notice if somebody later softens them into warnings.
 *
 *   node --test celestial/
 */

import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  BELT, DWELL, MODES, WHEEL, star, correspondence, reading, unspoken,
  validate, coverage, revise, history,
} from './atlas.js';
import { STARS, SOURCE, group, extractNote } from './stars.js';

// ----------------------------------------------------- the tonal layer

test('the seven modes are the seven diatonic modes', () => {
  assert.deepEqual(MODES.map((m) => m.name), [
    'Ionian', 'Dorian', 'Phrygian', 'Lydian',
    'Mixolydian', 'Aeolian', 'Locrian',
  ]);
});

test('each mode has the intervals music theory gives it', () => {
  // Written out here on purpose: atlas.js computes them by rotation, so an
  // independent list is what makes this a check rather than an echo.
  const expected = {
    Ionian: [0, 2, 4, 5, 7, 9, 11],
    Dorian: [0, 2, 3, 5, 7, 9, 10],
    Phrygian: [0, 1, 3, 5, 7, 8, 10],
    Lydian: [0, 2, 4, 6, 7, 9, 11],
    Mixolydian: [0, 2, 4, 5, 7, 9, 10],
    Aeolian: [0, 2, 3, 5, 7, 8, 10],
    Locrian: [0, 1, 3, 5, 6, 8, 10],
  };
  for (const mode of MODES) {
    assert.deepEqual([...mode.intervals], expected[mode.name], mode.name);
  }
});

test('every mode has seven degrees and none repeats a pitch', () => {
  for (const mode of MODES) {
    assert.equal(mode.intervals.length, 7, mode.name);
    assert.equal(new Set(mode.intervals).size, 7, mode.name);
  }
});

test('the wheel runs brightest to darkest, Lydian to Locrian', () => {
  assert.equal(WHEEL[0].name, 'Lydian');
  assert.equal(WHEEL[WHEEL.length - 1].name, 'Locrian');
  for (let i = 1; i < WHEEL.length; i += 1) {
    assert.ok(WHEEL[i - 1].brightness >= WHEEL[i].brightness,
      'brightness must not increase down the wheel');
  }
});

test('Locrian is the unstable edge, and that is measured not assigned', () => {
  // The surveyed fact under the intuition: it is the only diatonic mode with
  // no perfect fifth above the tonic, so its tonic triad is diminished.
  const unstable = MODES.filter((m) => !m.stable).map((m) => m.name);
  assert.deepEqual(unstable, ['Locrian']);
  assert.ok(!MODES.find((m) => m.name === 'Locrian').intervals.includes(7));
});

test('the tonal layer is surveyed, all of it', () => {
  for (const mode of MODES) assert.equal(mode.belt, BELT.SURVEYED, mode.name);
});

// ------------------------------------------------------- the sky layer

test('the sky is no longer empty, and every position is sourced', () => {
  // It stood empty while no catalogue was reachable, which was the honest
  // state then. It is a committed extract now, and the test that mattered
  // is unchanged in spirit: a position exists here only with its provenance.
  assert.ok(STARS.length > 0);
  assert.equal(coverage(STARS).skyAwaitingCatalogue, false);
  assert.equal(coverage([]).skyAwaitingCatalogue, true);

  for (const s of STARS) {
    assert.equal(s.belt, BELT.SURVEYED, s.name);
    assert.equal(s.source, SOURCE, s.name);
    assert.match(s.source, /J2000/, 'the epoch must be named, not implied');
  }
});

test('the extract says it is an extract', () => {
  // 28 of 9,096. A subset that does not announce itself reads as a sky, and
  // then absence in a drawing reads as absence in the world.
  assert.match(extractNote(), /extract, not the sky/);
  assert.match(extractNote(), /9,096/);
  assert.equal(group('bright-south').length + group('pleiades').length, STARS.length);
});

test('the committed positions are the ones the catalogue gives', () => {
  // Spot checks against values a reader can look up independently. If the
  // extraction script ever mangles a conversion, these are what notice.
  const at = (name) => STARS.find((s) => s.name === name);

  // Sirius, alpha Canis Majoris: 06h 45m 08.9s, -16d 42' 58" (J2000).
  assert.ok(Math.abs(at('Sirius').raHours - (6 + 45 / 60 + 8.9 / 3600)) < 1e-4);
  assert.ok(Math.abs(at('Sirius').decDegrees - -(16 + 42 / 60 + 58 / 3600)) < 1e-4);
  assert.equal(at('Sirius').magnitude, -1.46);

  // Acrux, the foot of the Southern Cross: 12h 26m 35.9s, -63d 05' 57".
  assert.ok(Math.abs(at('Acrux').raHours - (12 + 26 / 60 + 35.9 / 3600)) < 1e-4);
  assert.ok(Math.abs(at('Acrux').decDegrees - -(63 + 5 / 60 + 57 / 3600)) < 1e-4);

  // Every star inside the sky, and brighter numbers meaning brighter stars.
  for (const s of STARS) {
    assert.ok(s.raHours >= 0 && s.raHours < 24, s.name);
    assert.ok(s.decDegrees >= -90 && s.decDegrees <= 90, s.name);
  }
  // The two the seven-sisters research names are both present.
  assert.ok(at('Atlas') && at('Pleione'));
});

test('a star without a source is refused', () => {
  assert.throws(() => star({
    id: 'x', name: 'Some Star', raHours: 12.4, decDegrees: -63,
  }), /no source/);
});

test('a star with a source and sane coordinates is accepted', () => {
  const s = star({
    id: 'demo', name: 'Demonstration Star', raHours: 12.4, decDegrees: -63,
    magnitude: 1.3, source: 'illustrative only — not a catalogue reading',
  });
  assert.equal(s.belt, BELT.SURVEYED);
  assert.equal(s.source, 'illustrative only — not a catalogue reading');
});

test('coordinates outside the sky are refused', () => {
  const base = { id: 'x', name: 'X', source: 'test' };
  assert.throws(() => star({ ...base, raHours: 25, decDegrees: 0 }), /0–24/);
  assert.throws(() => star({ ...base, raHours: -1, decDegrees: 0 }), /0–24/);
  assert.throws(() => star({ ...base, raHours: 1, decDegrees: 91 }), /-90–90/);
  assert.throws(() => star({ ...base, raHours: 1, decDegrees: NaN }), /-90–90/);
});

// ------------------------------------------------ the correspondence

test('a correspondence is dreamed', () => {
  const c = correspondence({ mode: 'Lydian', region: 'the southern crown' });
  assert.equal(c.belt, BELT.DREAMED);
});

test('a correspondence cannot be filed as surveyed', () => {
  // The precise join where a personal atlas could start reading as an
  // astronomical claim. It is a throw rather than a coercion so that trying
  // is an error rather than a silently corrected habit.
  assert.throws(() => correspondence({
    mode: 'Lydian', region: 'the southern crown', belt: BELT.SURVEYED,
  }), /cannot be filed as surveyed/);
});

test('a correspondence must name a real mode', () => {
  assert.throws(() => correspondence({ mode: 'Hypolydian', region: 'anywhere' }),
    /not one of the seven/);
});

// -------------------------------------------------------- the refusal

test('an unlabeled entry is refused', () => {
  assert.throws(() => validate({ name: 'a line with no belt' }), /no belt/);
  assert.throws(() => validate({ belt: 'probably-fine' }), /no belt/);
  assert.throws(() => validate(null), /not an atlas entry/);
});

test('surveyed and dreamed entries both pass, which is the point', () => {
  // The rule is that a line declares which it is, not that one kind is
  // preferred. A register that only accepted surveyed lines would push the
  // dreamed ones into being unlabeled, which is the failure it exists to
  // prevent.
  assert.doesNotThrow(() => validate(MODES[0]));
  assert.doesNotThrow(() => validate(
    correspondence({ mode: 'Dorian', region: 'the river' })));
});

// ------------------------------------------------------------ readings

test('a reading holds several territories at different depths', () => {
  const r = reading({
    title: 'A Work', artist: 'Somebody',
    territories: [
      { mode: 'Mixolydian', dwell: DWELL.HOME },
      { mode: 'Lydian', dwell: DWELL.GLANCED },
    ],
  });
  assert.equal(r.territories.length, 2);
  assert.equal(r.territories[0].dwell, DWELL.HOME);
});

test('a reading records what a work refuses, not only what it enters', () => {
  // "The song refuses the night country" is a reading, not an absence. A
  // shape that stored only presence would discard the half of the
  // observation carrying the meaning.
  const r = reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Mixolydian', dwell: DWELL.HOME }],
    refuses: ['Locrian', 'Phrygian'],
  });
  assert.deepEqual([...r.refuses], ['Locrian', 'Phrygian']);
});

test('silence is distinguished from refusal', () => {
  const r = reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Mixolydian', dwell: DWELL.HOME }],
    refuses: ['Locrian'],
  });
  // Unmentioned modes are questions nobody answered; refused ones are answers.
  assert.ok(unspoken(r).includes('Lydian'));
  assert.ok(!unspoken(r).includes('Locrian'));
  assert.ok(!unspoken(r).includes('Mixolydian'));
});

test('a work cannot both enter and refuse the same territory', () => {
  assert.throws(() => reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
    refuses: ['Dorian'],
  }), /both enters and refuses/);
});

test('a territory without a depth is refused', () => {
  assert.throws(() => reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian' }],
  }), /without saying how deeply/);
});

test('a reading that places a work nowhere is refused', () => {
  assert.throws(() => reading({ title: 'A Work', artist: 'Somebody' }),
    /names no territory/);
});

test('a reading cannot be filed as surveyed', () => {
  assert.throws(() => reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
    belt: BELT.SURVEYED,
  }), /cannot be filed as surveyed/);
});

test('the readings written by hand fit the shape', async () => {
  // The point of the widening. If these stopped fitting, the structure has
  // drifted away from the practice it exists to hold.
  const { READINGS, territoryCounts } = await import('./readings.js');
  assert.ok(READINGS.length >= 2);
  for (const r of READINGS) {
    assert.equal(r.belt, BELT.DREAMED);
    assert.ok(r.territories.length >= 2, `${r.title} names one territory only`);
    assert.ok(r.paths, `${r.title} has no path character`);
    assert.ok(r.sky, `${r.title} has no sky`);
  }
  // This used to assert every reading had a *different* home mode, which
  // was true of the first two and is not a fact about anything. Lucky and
  // Hey There Delilah both live in Ionian, and there is no reason two works
  // should not share a climate — Ionian is the commonest home in this music,
  // so a collision was a matter of time. The old assertion would have forced
  // a reading to be rewritten to protect a coincidence, which is the tail
  // wagging the atlas.
  //
  // What was actually meant: each work has one climate, and the atlas can
  // tell the works apart. Both of those are real.
  for (const r of READINGS) {
    const homes = r.territories.filter((t) => t.dwell === DWELL.HOME);
    assert.equal(homes.length, 1,
      `${r.title} names ${homes.length} homes — a climate is where a work returns to`);
  }
  assert.ok(territoryCounts().get('Mixolydian') >= 1);
});

test('no reading reproduces lyrics in its prose', async () => {
  // A reading may quote a line in conversation. A repository holding song
  // text would be doing something else, and this is the guard on that.
  //
  // Titles and artists are excluded, and the exclusion is the point rather
  // than an escape hatch: a reading cannot exist without naming the work,
  // and pop titles are frequently lyric fragments — "Like I'm Gonna Lose
  // You" is one. The first version of this test scanned the whole record
  // and failed on the title, which would have meant either dropping the
  // guard or refusing to name the song. Naming a work is not reproducing it.
  //
  // It also caught its own author: a sky note here had echoed a line from
  // Shotgun. That is what it is for.
  const { READINGS } = await import('./readings.js');
  const prose = READINGS.map((r) => [
    r.centre, r.paths, r.sky,
    ...r.territories.map((t) => t.note ?? ''),
  ].join(' ')).join(' ').toLowerCase();

  for (const phrase of ['gotta hit the road', 'shotgun rider',
                        'gonna lose you', 'south of the equator',
                        'i\'ll be your', 'in love with my best friend',
                        'lucky to have been where i have been']) {
    assert.ok(!prose.includes(phrase), `lyric reproduced in prose: ${phrase}`);
  }
});

// -------------------------------------------------------------- the wheel

test('the wheel is laid out in brightness order, Lydian at the top', async () => {
  const { wheelGeometry } = await import('./wheel.js');
  const spots = wheelGeometry({ radius: 100 });

  assert.equal(spots[0].mode, 'Lydian');
  assert.equal(spots[0].degrees, 270, 'brightest sits at the top');
  assert.equal(spots[spots.length - 1].mode, 'Locrian');
  assert.equal(spots.length, 7);
});

test('the seven territories are evenly spaced', async () => {
  const { wheelGeometry } = await import('./wheel.js');
  const spots = wheelGeometry({ radius: 100 });
  const gaps = spots.slice(1).map((s, i) =>
    ((s.degrees - spots[i].degrees) + 360) % 360);

  for (const gap of gaps) assert.ok(Math.abs(gap - 360 / 7) < 1e-9);
});

test('the layout comes from the intervals, not a hand-written order', async () => {
  // If somebody reorders the wheel for looks, the arithmetic and the picture
  // stop agreeing, and this is what notices.
  const { wheelGeometry } = await import('./wheel.js');
  const spots = wheelGeometry();
  for (let i = 1; i < spots.length; i += 1) {
    assert.ok(spots[i - 1].brightness >= spots[i].brightness,
      `${spots[i - 1].mode} should not be dimmer than ${spots[i].mode}`);
  }
});

test('a refused territory is drawn and struck, never omitted', async () => {
  const { drawReading } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  const shotgun = READINGS.find((r) => r.title === 'Shotgun');
  const svg = drawReading(shotgun);

  // Absence would render "the song will not go here" identically to silence.
  for (const mode of shotgun.refuses) {
    assert.ok(svg.includes(`>${mode}</text>`), `${mode} is missing from the drawing`);
  }
  assert.ok(svg.includes('class="struck"'), 'refusals are marked as refusals');
});

test('every one of the seven appears, whatever the reading says', async () => {
  const { drawReading } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  for (const read of READINGS) {
    const svg = drawReading(read);
    for (const mode of MODES) {
      assert.ok(svg.includes(`>${mode.name}</text>`),
        `${read.title}: ${mode.name} missing`);
    }
  }
});

test('the drawing declares itself dreamed on its face', async () => {
  // A diagram travels further than the file it came from and arrives
  // without context, so it carries the label rather than relying on one.
  const { drawReading, DRAWING_BELT } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  assert.equal(DRAWING_BELT, BELT.DREAMED);
  assert.match(drawReading(READINGS[0]), /dreamed line — not an astronomical chart/);
});

test('the mode wheel draws no stars, catalogue or not', async () => {
  const { drawReading, skyNotice } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  const svg = drawReading(READINGS[0]);

  // This used to read "while the catalogue is missing". The catalogue is no
  // longer missing and the assertion still holds, which is the point: the
  // wheel is a diagram of tonal territory, not a star chart, and scattering
  // real positions across it would be a category error rather than a
  // fabrication. Real coordinates in the wrong frame are no better than
  // invented ones — arguably worse, since they survive being checked.
  assert.ok(!/star/i.test(svg.replace(/<desc>[\s\S]*?<\/desc>/, '')),
    'the mode wheel must not render anything star-shaped');

  // The notice tracks the real state rather than a remembered one.
  assert.match(skyNotice([]), /no stars yet/);
  assert.match(skyNotice(STARS), new RegExp(`^${STARS.length} stars`));
});

test('a rehearing keeps the hearing it replaces', () => {
  // A reading is how somebody hears a work on a day. Before revise(), the
  // only way to record a changed hearing was to edit the reading — which
  // destroyed the earlier one and left the atlas presenting its latest
  // opinion as the only one there had ever been.
  const first = reading({
    title: 'A Work', artist: 'Somebody', asOf: '2016-03-01',
    territories: [{ mode: 'Aeolian', dwell: DWELL.HOME }],
    refuses: ['Locrian'],
  });
  const later = revise(first, {
    asOf: '2026-08-11',
    territories: [
      { mode: 'Ionian', dwell: DWELL.HOME },
      { mode: 'Aeolian', dwell: DWELL.GLANCED },
    ],
  });

  const chain = history(later);
  assert.equal(chain.length, 2);
  assert.deepEqual(chain.map((r) => r.asOf), ['2016-03-01', '2026-08-11']);

  // The earlier hearing is untouched, not merely remembered as a diff.
  assert.equal(chain[0].territories[0].mode, 'Aeolian');
  assert.equal(chain[0].territories[0].dwell, DWELL.HOME);
  // Fields not named in the revision carry forward.
  assert.deepEqual([...later.refuses], ['Locrian']);
  // A reading with no revisions is a chain of one, not an error.
  assert.equal(history(first).length, 1);
});

test('a rehearing without a date is refused', () => {
  // The whole purpose is sequence. An undated revision cannot take a place
  // in the order it exists to record, and would silently become "latest".
  const first = reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
  });
  assert.throws(() => revise(first, { paths: 'different now' }), /needs an asOf/);
  assert.throws(() => revise(null, { asOf: '2026-01-01' }), /needs the reading/);

  // And a revision is still a reading: the same refusals apply to it.
  assert.throws(() => revise(first, {
    asOf: '2026-01-01', refuses: ['Dorian'],
  }), /both enters and refuses/);
});

test('depth changes how far a ray reaches', async () => {
  const { drawReading } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  const delilah = READINGS.find((r) => r.title === 'Hey There Delilah');
  const svg = drawReading(delilah);

  assert.ok(svg.includes('class="ray home"'));
  assert.ok(svg.includes('class="ray through"'));
  assert.ok(svg.includes('class="ray glanced"'),
    'a glanced territory should still be drawn, shorter');
});

test('entered-but-not-dwelt is not the same as refused', async () => {
  // Hey There Delilah passes through the night country and will not settle
  // there. That is glanced, not refused, and the shape keeps them apart.
  const { READINGS } = await import('./readings.js');
  const delilah = READINGS.find((r) => r.title === 'Hey There Delilah');
  const aeolian = delilah.territories.find((t) => t.mode === 'Aeolian');

  assert.equal(aeolian.dwell, DWELL.GLANCED);
  assert.ok(!delilah.refuses.includes('Aeolian'));
});

test('every ray says which territory it belongs to', async () => {
  // Found by rendering, not by reading. Length alone carries depth, and a
  // glanced ray is short — drawn with nothing else it was a faint stub near
  // the centre that a viewer could not attribute to any mode. The picture
  // was silently dropping the glanced/refused distinction the data keeps.
  const { drawReading, wheelGeometry } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  const delilah = READINGS.find((r) => r.title === 'Hey There Delilah');
  const size = 520;
  const svg = drawReading(delilah, { size });

  const mid = size / 2;
  const spots = new Map(
    wheelGeometry({ radius: size * 0.36 }).map((s) => [s.mode, s]));

  for (const t of delilah.territories) {
    const spot = spots.get(t.mode);
    const x = (mid + spot.x).toFixed(1);
    const y = (mid + spot.y).toFixed(1);
    assert.ok(
      svg.includes(`<line x1="${mid}" y1="${mid}" x2="${x}" y2="${y}" ` +
                   `class="toward ${t.dwell}"`),
      `${t.mode} is placed but nothing reaches its marker — the ray points ` +
      `at a territory the drawing never names`);
  }
});

test('a refused territory gets no line toward it', async () => {
  // The mirror of the test above. Reaching toward a refusal would read as
  // "the work goes here, faintly", which is the opposite of what was said.
  const { drawReading } = await import('./wheel.js');
  const { READINGS } = await import('./readings.js');
  const shotgun = READINGS.find((r) => r.title === 'Shotgun');
  const svg = drawReading(shotgun);

  const toward = svg.match(/class="toward [a-z]+"/g) ?? [];
  assert.equal(toward.length, shotgun.territories.length,
    'exactly one line per entered territory, and none for the refused ones');
});

test('a work cannot both enter and refuse the same territory', async () => {
  // Not hypothetical. The reading for "Lucky" arrived saying Aeolian
  // "appears only as a distant memory" *and* that the song "does not visit
  // the night country" — which is Aeolian in this atlas's vocabulary. Both
  // sentences are natural to write and they cannot both be filed.
  //
  // A shape that accepted this would keep whichever field happened to be
  // read last, silently, and the reader afterwards could not tell a
  // considered glance from a considered refusal.
  assert.throws(() => reading({
    title: 'Lucky', artist: 'Jason Mraz, feat. Colbie Caillat',
    territories: [
      { mode: 'Ionian', dwell: DWELL.HOME },
      { mode: 'Aeolian', dwell: DWELL.GLANCED },
    ],
    refuses: ['Aeolian'],
  }), /both enters and refuses Aeolian/);
});

test('the four readings agree on what the night country is', async () => {
  // The territory vocabulary is prose, so it can drift while every
  // structural test still passes — Aeolian could quietly become something
  // else in a later reading and nothing would object. Three readings place
  // Aeolian and all three call it the night country or its shadow; this
  // pins that they keep meaning the same region.
  const { READINGS } = await import('./readings.js');
  const aeolian = READINGS
    .map((r) => r.territories.find((t) => t.mode === 'Aeolian'))
    .filter(Boolean);

  assert.ok(aeolian.length >= 3, 'expected Aeolian placed in several readings');
  for (const t of aeolian) {
    assert.match(t.note, /night country|shadow|dark/i,
      `Aeolian described as something else: ${t.note}`);
  }
});

test('the atlas reports the works it cannot tell apart', async () => {
  // Deliberately not a test that collisions are absent. Two readings do
  // collide — Hey There Delilah and Lucky place identically, and their
  // wheels are the same drawing with a different name on it. Forbidding
  // that would have made the vocabulary's coarseness look like a mistake in
  // somebody's reading, and the obvious way to silence it is to edit the
  // reading until the instrument stops complaining.
  //
  // So the limit is reported instead. This test holds that it *stays*
  // reported: a collision must not become invisible by being ignored.
  const { READINGS, collisions } = await import('./readings.js');
  const found = collisions();

  const colliding = new Set(found.flat());
  assert.ok(colliding.has('Hey There Delilah') && colliding.has('Lucky'),
    'the known collision is no longer reported — either the vocabulary grew ' +
    'a distinction, in which case say so here, or the report broke');

  // Every group is a real group, and nothing is quietly listed alone.
  for (const group of found) assert.ok(group.length > 1);
  // And a set of readings with nothing in common reports nothing.
  assert.deepEqual(collisions(READINGS.slice(0, 2)), []);
});

test('the reserved word does not enter this layer', async () => {
  // Indigenous-Data-Sovereignty.md: "Songline" is never a component name. It
  // belongs to the First Peoples of this land, not to a piece of software;
  // Starline and Dreamline are this project's own coinages.
  //
  // This is a test rather than a note because the rule has now been reached
  // for twice in incoming readings, both times as a section heading — which
  // is the position that becomes a field name. Catching it by remembering
  // works until the once it doesn't, and the project's own line is that
  // consent and constraint are runtime properties, not documents. So the
  // layer refuses the word the way BusHub refuses unlabeled speech.
  const fs = await import('node:fs/promises');
  const dir = new URL('.', import.meta.url);
  const files = (await fs.readdir(dir)).filter((f) => /\.(js|html|md)$/.test(f));

  for (const file of files) {
    const text = await fs.readFile(new URL(file, dir), 'utf8');
    for (const [i, line] of text.split('\n').entries()) {
      // The rule names the word; this test is the one place allowed to
      // quote it, in the comment above and in this pattern.
      if (/\bsonglines?\b/i.test(line) && !/Indigenous-Data-Sovereignty|never a component name|reserved word/i.test(line)) {
        assert.fail(`${file}:${i + 1} uses the reserved word — say Starline ` +
                    `(the map) or Dreamline (the traveller): ${line.trim()}`);
      }
    }
  }
});

test('the atlas measures how much of itself is structural', async () => {
  const { resolution, collisions } = await import('./readings.js');
  const r = resolution();

  assert.equal(r.readings, 9);
  assert.equal(r.distinctPlacements, 7);
  assert.equal(r.indistinguishable, 2);

  // What the motion vocabulary actually bought, rather than what it was
  // hoped to buy: three placements become four, and one collision survives.
  // Hey There Delilah and Lucky still land together, because what separates
  // them is reciprocity — one person reaching across a distance against two
  // walking side by side — and that is a fact about the relationship, not
  // about the shape of the paths. Inventing a fourth axis to force them
  // apart would be fitting the instrument to the answer.
  assert.equal(r.distinctWithMotion, 8);
  assert.equal(r.stillIndistinguishable, 1);

  // The two figures are the same fact seen twice, so they must agree.
  const collapsed = collisions().reduce((n, g) => n + g.length - 1, 0);
  assert.equal(collapsed, r.indistinguishable,
    'the collision report and the resolution figure disagree');
});

test('the atlas refuses to hold the same work twice', async () => {
  // Not hypothetical: a reading was pasted in twice, and the machinery
  // reported the duplicate as "Photograph == Photograph — placed identically
  // by this vocabulary", with resolution() counting six readings and three
  // placements. A mistake wearing the shape of a finding, produced by the
  // functions written to be honest about limits. This is the guard.
  const { register, reading, DWELL } = await import('./atlas.js');
  const one = reading({
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
  });
  const sameAgain = reading({
    title: 'a work', artist: 'SOMEBODY',   // case must not smuggle it past
    territories: [{ mode: 'Lydian', dwell: DWELL.HOME }],
  });

  assert.throws(() => register([one, sameAgain]), /already in the atlas/);
  assert.doesNotThrow(() => register([one]));

  // Same title, different artist is a different work and must pass.
  const cover = reading({
    title: 'A Work', artist: 'Somebody Else',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
  });
  assert.doesNotThrow(() => register([one, cover]));
});

test('a collision report can only be about distinct works', async () => {
  // The guarantee collisions() leans on. If register() ever stopped
  // refusing duplicates, every collision report would become ambiguous
  // between a vocabulary limit and a filing error.
  const { READINGS, collisions } = await import('./readings.js');
  const names = READINGS.map((r) => `${r.title} ${r.artist}`.toLowerCase());
  assert.equal(new Set(names).size, names.length);

  for (const group of collisions()) {
    assert.equal(new Set(group).size, group.length,
      'a title appears twice inside one collision group');
  }
});

test('no source file carries a control character', async () => {
  // A stray NUL byte reached atlas.js and was committed. It parsed, ran, and
  // passed every test — the key it sat in worked perfectly well. What it did
  // was make the file *binary* to ripgrep, so a directory-wide content search
  // silently skipped the one file holding the belt rules and the star
  // provenance check. Not a crash: a hole in the tooling, invisible from the
  // code and invisible from the test output.
  //
  // Tabs, newlines and carriage returns are the only control characters a
  // source file has business containing.
  const fs = await import('node:fs/promises');
  const dir = new URL('.', import.meta.url);
  const files = (await fs.readdir(dir)).filter((f) => /\.(js|html|md)$/.test(f));

  for (const file of files) {
    const bytes = await fs.readFile(new URL(file, dir));
    for (const [i, byte] of bytes.entries()) {
      const printable = byte >= 0x20 || byte === 0x09 || byte === 0x0a || byte === 0x0d;
      assert.ok(printable,
        `${file} byte ${i}: control character 0x${byte.toString(16).padStart(2, '0')} — ` +
        `it will not show in a diff and makes the file binary to search tools`);
    }
  }
});

test('motion uses a closed vocabulary or none at all', async () => {
  const { reading, DWELL, MOTION } = await import('./atlas.js');
  const base = {
    title: 'A Work', artist: 'Somebody',
    territories: [{ mode: 'Dorian', dwell: DWELL.HOME }],
  };

  // Absent is fine — the field is optional on purpose.
  assert.equal(reading({ ...base }).motion, undefined);

  const full = reading({ ...base, motion: {
    reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY,
    shape: MOTION.SHAPE.RETURNS,
  } });
  assert.equal(full.motion.shape, 'returns');

  // Half-filled is refused: it would be counted as a distinction that was
  // never actually made.
  assert.throws(() => reading({ ...base, motion: {
    reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY } }), /motion\.shape/);
  assert.throws(() => reading({ ...base, motion: {
    reach: 'quite far', pace: MOTION.PACE.STEADY,
    shape: MOTION.SHAPE.RETURNS } }), /motion\.reach/);
});

test('the unvisited territory is the one the arithmetic calls unstable', async () => {
  // Two layers agreeing without being made to. The readings are written by
  // ear; hasPerfectFifth is interval arithmetic. Nobody consulted the second
  // while writing the first, and the only mode no work has entered is the
  // only mode with no perfect fifth above its tonic.
  //
  // Held as a test so that it stays *checked* rather than becoming a nice
  // sentence somebody repeats. If a later reading enters Locrian, this fails
  // and the claim gets rewritten instead of quietly outliving its truth.
  const { frontier } = await import('./readings.js');
  const f = frontier();

  assert.deepEqual(f.unvisited, ['Locrian']);
  const unstable = MODES.filter((m) => !m.stable).map((m) => m.name);
  assert.deepEqual(f.unvisited, unstable);

  // Phrygian was refused-only until the sixth reading entered it.
  assert.ok(f.entered.includes('Phrygian'));
  assert.deepEqual(f.refusedOnly, ['Locrian']);
  // Every mode has now been spoken about one way or the other.
  assert.deepEqual(f.neverMentioned, []);
});

// -------------------------------------------------------- the cycle chart

test('the cycle chart carries its attribution on the drawing itself', async () => {
  // The condition under which this was built. Implementing a named author's
  // published form while dropping the name removes the acknowledgment, not
  // the borrowing — and a credit in a caption is a credit that gets cropped.
  const { cycle, drawCycle, AFTER, CITATION } = await import('./cycle.js');
  const svg = drawCycle(cycle({ name: 'Empty' }));

  assert.match(AFTER, /Connie Cockrell Kaplan/);
  assert.match(AFTER, /Woman's Book of Dreams/);
  assert.match(svg, /Kaplan/, 'the credit must be in the drawing, not beside it');
  // Before the wedges, not after them.
  assert.ok(svg.indexOf('Kaplan') < svg.indexOf('class="day'));

  // The book is confirmed from a photograph of its cover. The imprint is not
  // — publisher, year and ISBN are catalogue records rather than the title
  // page, and they stay separated so the weaker half cannot inherit the
  // strength of the better half. That inheritance is how a provenance goes
  // missing, and this citation has already done it once: the book was named
  // on a search match with the inferential step removed, and the guess
  // happening to be right does not make it not a guess.
  assert.equal(CITATION.confirmed, true);
  assert.equal(CITATION.author, 'Connie Cockrell Kaplan');
  assert.ok(CITATION.fromTheObject.includes('title'));

  // The copyright page corrected the one field that had been flagged as
  // weaker than the rest, and it is the reason the split exists. The ISBN
  // carried from catalogue records was 1-58270-008-7 — the Beyond Words
  // printing, a real ISBN for a different book than the copy in hand, which
  // is "This Edition Printed For Axiom Publishing, 2000". No amount of
  // re-reading the sentence would have caught that.
  assert.equal(CITATION.isbn, '1-86476-056-7 (pbk.)');
  assert.match(CITATION.edition, /Axiom Publishing, 2000/);
  assert.equal(CITATION.supersededByTheObject.isbn, '1-58270-008-7');
  assert.ok(CITATION.fromTheObject.includes('isbn'),
    'the ISBN is now read off the object and says so');
  assert.ok(CITATION.assumed, 'and the remaining assumption is named');
  assert.ok(!/1-58270-008-7/.test(AFTER),
    'the drawn credit names what was seen, not what was looked up');
});

test('a blank day and a void day are not the same day', async () => {
  // The distinction the chart was worth building for, and the one the
  // original arrived at independently: a marked absence is a reading, an
  // unmarked one is silence.
  const { cycle, day, drawCycle, tally, MARK } = await import('./cycle.js');
  const c = cycle({ days: [day({ number: 3, mark: MARK.VOID })] });

  const t = tally(c);
  assert.equal(t.days, 29);
  assert.equal(t.void, 1);
  assert.equal(t.blank, 28);

  const svg = drawCycle(c);
  assert.equal((svg.match(/class="struck"/g) ?? []).length, 1,
    'exactly the void day is struck');
  assert.match(svg, /class="day void"/);
  assert.match(svg, /class="day blank"/);
});

test('every wedge exists before anything is written in it', async () => {
  // A chart that grew a day only when somebody wrote in it could not show
  // the shape of a quiet month, and the shape of a quiet month is a reading.
  const { cycle, CYCLE_DAYS } = await import('./cycle.js');
  const c = cycle();
  assert.equal(c.days.length, CYCLE_DAYS);
  assert.deepEqual(c.days.map((d) => d.number),
    Array.from({ length: CYCLE_DAYS }, (_, i) => i + 1));
});

test('a recorded day that says nothing is refused', async () => {
  const { day, cycle, MARK } = await import('./cycle.js');

  assert.throws(() => day({ number: 1, mark: MARK.RECORDED }), /says nothing/);
  assert.throws(() => day({ number: 1, mark: MARK.VOID, note: 'something' }),
    /carries a note/);
  assert.throws(() => day({ number: 0 }), /runs 1–29/);
  assert.throws(() => day({ number: 30 }), /runs 1–29/);
  assert.throws(() => day({ number: 1, mark: 'maybe' }), /use recorded/);
  assert.throws(() => cycle({ days: [day({ number: 2 }), day({ number: 2 })] }),
    /appears twice/);

  assert.doesNotThrow(() => day({ number: 1, mark: MARK.RECORDED, note: 'a dream' }));
});

test('the empty chart says it is empty, and why', async () => {
  // The same move as the sky layer while no catalogue was reachable: a gap
  // that names itself is a known gap, and a blank panel is not.
  const { cycle, cycleNotice, drawCycle } = await import('./cycle.js');
  const c = cycle();

  assert.match(cycleNotice(c), /none of them written in/);
  assert.match(cycleNotice(c), /somebody's dreams/);
  // And it is a dreamed line, said on its face — but not an astronomical one.
  assert.match(drawCycle(c), /dreamed line — a record of dreaming, not of the sky/);
});

test('the fourth motion shape waited for its second example', async () => {
  // "This Is Me" arrived with a shape MOTION.SHAPE could not name: the centre
  // is a waypoint, climbed to and then gone out from — not departs, not
  // returns, not shuttles. It was filed with **no motion at all** rather than
  // forced into the nearest value, and the source comment said a second
  // example would be the evidence for adding one.
  //
  // "Firework" is that second example: start low, explode outward from the
  // centre, described in different words by a different work. RADIATES was
  // added then, not before.
  //
  // This test holds the restraint rather than the result. Two independent
  // readings carry it; if a fifth shape is ever proposed, it should have to
  // clear the same bar.
  const { MOTION } = await import('./atlas.js');
  const { READINGS } = await import('./readings.js');

  assert.equal(MOTION.SHAPE.RADIATES, 'radiates');
  const radiating = READINGS.filter((r) => r.motion?.shape === MOTION.SHAPE.RADIATES);
  assert.ok(radiating.length >= 2,
    'radiates exists because two readings asked for it — if it is ever down ' +
    'to one, the value is being kept for a single case');
  assert.deepEqual(radiating.map((r) => r.title).sort(),
    ['Firework', 'This Is Me']);

  // Both describe the same movement, and neither says the other's words.
  for (const r of radiating) assert.match(r.paths, /start low/);
});

test('a stated refusal and an absent one are different readings', async () => {
  // The distinction earns itself here rather than in the abstract.
  // "Firework" places its territories identically to "Hey There Delilah" and
  // "Lucky". Those two refuse Phrygian and Locrian; Firework names no
  // refusal at all. The only thing separating three readings is that two
  // spoke and one did not.
  //
  // A shape that treated absent-refusal as refusal — or as nothing — would
  // have collapsed them into one.
  const { unspoken } = await import('./atlas.js');
  const { READINGS, collisions } = await import('./readings.js');

  const firework = READINGS.find((r) => r.title === 'Firework');
  const delilah = READINGS.find((r) => r.title === 'Hey There Delilah');

  const territories = (r) => r.territories.map((t) => `${t.mode}:${t.dwell}`).sort();
  assert.deepEqual(territories(firework), territories(delilah),
    'the premise of this test: identical territories');

  assert.deepEqual([...firework.refuses], []);
  assert.deepEqual([...delilah.refuses], ['Phrygian', 'Locrian']);

  // So Phrygian and Locrian are questions here and answers there.
  assert.deepEqual(unspoken(firework).sort(), ['Locrian', 'Phrygian']);
  assert.deepEqual(unspoken(delilah), []);

  // And the atlas keeps them apart.
  const together = collisions().find((g) =>
    g.includes('Firework') && g.includes('Hey There Delilah'));
  assert.equal(together, undefined,
    'silence and refusal must not be reported as the same placement');
});
