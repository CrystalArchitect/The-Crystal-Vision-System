/**
 * Readings — works placed on the wheel.
 *
 * Every entry here is a dreamed line and says so. The modes underneath are
 * arithmetic and the sky will be a catalogue; that a particular song lives
 * in Mixolydian is somebody's ear, offered rather than measured. Nobody
 * else has to hear it that way, and the shape is built so a later reader
 * cannot mistake these for analysis of the recordings.
 *
 * These three were written by hand before this file existed, and they are
 * what showed the original single mode-to-region correspondence was too
 * thin: each names several territories at different depths, each says which
 * territories the work will not enter, and each gives the paths a shape.
 * The structure was widened to fit the practice rather than the practice
 * trimmed to fit the structure.
 *
 * No lyrics are stored. A reading may quote a line in conversation; a
 * repository holding song text would be doing something else entirely, and
 * the mapping is the part that belongs to whoever made it.
 */

import { DWELL, MOTION, reading, register } from './atlas.js';

export const READINGS = register([
  reading({
    title: 'Shotgun',
    artist: 'George Ezra',
    centre: 'Not a person: the act of leaving, and the road itself. Pure ' +
            'forward motion and open horizon.',
    territories: [
      { mode: 'Mixolydian', dwell: DWELL.HOME,
        note: 'The open roads and crossroads. Bright, driving, major-key ' +
              'restlessness — the whole song sits here.' },
      { mode: 'Ionian', dwell: DWELL.THROUGH,
        note: 'The clear daylight plains. The big sunny choruses, ' +
              'uncomplicated joy of movement.' },
      { mode: 'Lydian', dwell: DWELL.GLANCED,
        note: 'The high bright uplands — the lifted, almost weightless ' +
              'feeling where the horizon seems higher than usual.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills just beyond the known. A travel-worn ' +
              'quality under the brightness of the verses.' },
    ],
    refuses: ['Aeolian', 'Phrygian', 'Locrian'],
    paths: 'Long, straight, high-speed lines running from the centre toward ' +
           'the horizon. No looping back, no complicated return — just the ' +
           'continuous act of going.',
    // "no looping back" — the only reading here that never comes home.
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.URGENT,
              shape: MOTION.SHAPE.DEPARTS },
    sky: 'A bright, fast-moving figure low on the horizon: the kind you ' +
         'watch while the car is already in motion. It does not ask you to ' +
         'stop and interpret. It asks you to get in and ride. The southern ' +
         'framing is the work\'s own, and so is the role it hands the ' +
         'traveller — the one who reads the map and keeps the course, ' +
         'rather than the one merely carried.',
  }),

  reading({
    title: 'Like I\'m Gonna Lose You',
    artist: 'Meghan Trainor, feat. John Legend',
    centre: 'The relationship itself under quiet threat. Not departure: the ' +
            'fear of absence, and the decision to hold on tighter.',
    territories: [
      { mode: 'Aeolian', dwell: DWELL.HOME,
        note: 'The deep forests and night country. Minor-key tenderness, ' +
              'the sense that something precious could slip away in the dark.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills beyond the known. The gentle lift that ' +
              'keeps the sadness from becoming despair.' },
      { mode: 'Ionian', dwell: DWELL.THROUGH,
        note: 'The clear daylight plains the choruses reach toward — the ' +
              'vow to love harder now, while the light still holds.' },
      { mode: 'Mixolydian', dwell: DWELL.GLANCED,
        note: 'Brief flashes of forward resolve that always return to the ' +
              'night country.' },
    ],
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Short, urgent loops between the night forest and the clear ' +
           'plains. They do not travel far. They keep circling the centre — ' +
           'choosing the person again and again before the light changes.',
    motion: { reach: MOTION.REACH.NEAR, pace: MOTION.PACE.URGENT,
              shape: MOTION.SHAPE.RETURNS },
    sky: 'A close, intimate figure: two stars held in a tight orbit low in ' +
         'the southern sky. Vigilance and devotion rather than distance or ' +
         'speed.',
  }),
  reading({
    title: 'Hey There Delilah',
    artist: "Plain White T's",
    centre: 'Long-distance devotion. Two people held in the same frame while ' +
            'separated by cities and time zones, and the quiet promise that ' +
            'the distance is temporary.',
    territories: [
      { mode: 'Ionian', dwell: DWELL.HOME,
        note: 'The clear daylight plains. Bright, major-key sincerity — the ' +
              'open-hearted letters and late-night calls.' },
      { mode: 'Mixolydian', dwell: DWELL.THROUGH,
        note: 'The open roads. Travelling and working and moving through the ' +
              'world while still oriented toward the other person.' },
      { mode: 'Lydian', dwell: DWELL.THROUGH,
        note: 'The high bright uplands — a luminous quality in the melody, ' +
              'hope sitting above ordinary ground.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. A steady warmth that keeps the brightness ' +
              'from turning purely sentimental.' },
      // Entered, and not dwelt in. The reading says the song refuses to
      // *stay* in the night country, which is not the same as refusing to
      // go there — so it is glanced rather than refused, and the vocabulary
      // already had the word for it.
      { mode: 'Aeolian', dwell: DWELL.GLANCED,
        note: 'Brief shadows: the loneliness of the distance. The song ' +
              'passes through and will not settle here.' },
    ],
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Long, patient arcs stretching across the circle and always ' +
           'returning to the centre. Slow lines — the kind you can follow ' +
           'for years without losing the signal.',
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY,
              shape: MOTION.SHAPE.RETURNS },
    sky: 'A pair of stars in a wide but stable orbit, visible from either ' +
         'hemisphere. Endurance rather than speed or urgency.',
  }),

  reading({
    title: 'Lucky',
    artist: 'Jason Mraz, feat. Colbie Caillat',
    centre: 'Quiet, mutual astonishment. Two people looking at each other ' +
            'and recognising that the odds landed in their favour — love ' +
            'and friendship arriving in the same person.',
    territories: [
      { mode: 'Ionian', dwell: DWELL.HOME,
        note: 'The clear daylight plains. Warm major-key contentment; soft, ' +
              'steady sunlight rather than a burst of it.' },
      { mode: 'Lydian', dwell: DWELL.THROUGH,
        note: 'The high bright uplands — the gentle lift in the melody, ' +
              'ordinary life quietly elevated.' },
      { mode: 'Mixolydian', dwell: DWELL.THROUGH,
        note: 'The open roads. Easy, unforced forward motion: no urgency, ' +
              'just the pleasure of walking the same path.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. A soft earthy undercurrent keeping the ' +
              'sweetness grounded.' },
      // As written, this reading said Aeolian "appears only as a distant
      // memory of loneliness" and that the song "does not visit the night
      // country" — which is Aeolian, in this atlas's own vocabulary. The
      // shape refused it: both enters and refuses Aeolian, one of the two
      // is wrong. Resolved the same way Hey There Delilah was: an
      // appearance is an entry, however brief, and not dwelling is not
      // refusing. A distant memory is still a memory the song has.
      { mode: 'Aeolian', dwell: DWELL.GLANCED,
        note: 'A distant memory of loneliness, held at arm\'s length. The ' +
              'song remembers the night country without going back to it.' },
    ],
    // "The dissolving edges" — Locrian is literally that, the only mode with
    // no perfect fifth to hold its tonic still.
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Long, gentle, interlocking arcs that keep returning to the ' +
           'centre. Slow and reciprocal — the kind two people can walk ' +
           'side by side for years without either one leading.',
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY,
              shape: MOTION.SHAPE.RETURNS },
    sky: 'A close double star, low and unhurried. Where the other pairs in ' +
         'this atlas are holding on or holding out, this one is simply ' +
         'in orbit and has been for a long time.',
  }),

  reading({
    title: 'Photograph',
    artist: 'Ed Sheeran',
    centre: 'Memory held in the hand. An image that keeps someone present ' +
            'long after the moment it was taken has gone.',
    territories: [
      { mode: 'Aeolian', dwell: DWELL.HOME,
        note: 'The deep forests and night country. Soft minor-key longing — ' +
              'the quiet ache of distance and time.' },
      { mode: 'Ionian', dwell: DWELL.THROUGH,
        note: 'The clear daylight plains the choruses reach toward: the ' +
              'decision to keep loving through the image.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. Gentle supportive warmth that keeps the ' +
              'sadness from turning heavy.' },
      { mode: 'Mixolydian', dwell: DWELL.GLANCED,
        note: 'Brief forward-looking resolve before the song returns to the ' +
              'quieter forest.' },
    ],
    // Written as "Phrygian and Locrian remain at the outer edge", which is
    // softer than the outright refusals in the earlier readings. Filed as
    // refused on the strength of the sentence after it — the song
    // acknowledges absence without dissolving into it, and Locrian is the
    // dissolving one. If that was meant as silence rather than refusal, it
    // belongs in neither list and this is the line to change.
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Slow, looping paths between the night forest and the clear ' +
           'plains, always carrying the same object between them. The kind ' +
           'that let you revisit a place without leaving where you are.',
    // Runs between two territories rather than home to the centre.
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY,
              shape: MOTION.SHAPE.SHUTTLES },
    sky: 'A single steady point that stays where it was after the others ' +
         'have shifted. The first reading here to name one star rather ' +
         'than a pair.',
  }),

  reading({
    title: 'Someone You Loved',
    artist: 'Lewis Capaldi',
    asOf: '2026-08-11',
    centre: 'Abrupt absence. The moment the person who was the centre of ' +
            'gravity is simply gone, and the ground has not been replaced ' +
            'with anything.',
    territories: [
      { mode: 'Aeolian', dwell: DWELL.HOME,
        note: 'The deep forests and night country. Heavy minor-key grief — ' +
              'the song barely leaves this climate.' },
      // The first work in this atlas to enter Phrygian. The five before it
      // all refuse the mode outright, so the shadowed borderlands had been
      // named only by what would not go there.
      { mode: 'Phrygian', dwell: DWELL.GLANCED,
        note: 'The shadowed borderlands. Brief darker colourings that push ' +
              'the ache toward instability without crossing into it.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. Softens the despair just enough to keep ' +
              'the melody human rather than crushed.' },
      { mode: 'Ionian', dwell: DWELL.GLANCED,
        note: 'The clear daylight plains, appearing only as remembered or ' +
              'longed for — the light that is not present any more.' },
    ],
    // "Approaches the dissolving boundary but does not enter it" — refusal,
    // and Locrian is literally the dissolving one: no perfect fifth to hold
    // its tonic still.
    refuses: ['Locrian'],
    paths: 'Short, broken, inward-folding paths that keep trying to return ' +
           'to a centre that is no longer there. They still point at the ' +
           'place, and the place has gone dark.',
    motion: { reach: MOTION.REACH.NEAR, pace: MOTION.PACE.URGENT,
              shape: MOTION.SHAPE.RETURNS },
    sky: 'A once-bright point that has dimmed or dropped below the horizon. ' +
         'Named as a felt image, not as any star in the extract next door.',
  }),

  reading({
    title: 'Viva la Vida',
    artist: 'Coldplay',
    asOf: '2026-08-11',
    centre: 'The fallen throne. Someone who held the world and now walks the ' +
            'street alone, with the authority gone and the person left over.',
    territories: [
      { mode: 'Aeolian', dwell: DWELL.HOME,
        note: 'The deep forests and night country. The prevailing minor-key ' +
              'atmosphere of loss and exile.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. A steady, almost march-like dignity that ' +
              'keeps the melancholy from collapsing into despair.' },
      { mode: 'Mixolydian', dwell: DWELL.THROUGH,
        note: 'The open roads. The driving, anthemic lift of the chorus — ' +
              'the memory of power still moving forward.' },
      { mode: 'Ionian', dwell: DWELL.GLANCED,
        note: 'The clear daylight plains, in brief flashes only: the former ' +
              'glory, remembered rather than held.' },
    ],
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Long, processional lines running from a high centre outward into ' +
           'exile, then circling back as memory. Royal roads walked on foot.',
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.STEADY,
              shape: MOTION.SHAPE.RETURNS },
    // Note the inversion against the other Aeolian-home readings: there the
    // forward mode is glanced and the daylight is passed through. Here it is
    // the other way about — the drive is real and the daylight is only
    // remembered, which is what makes it an exile rather than a grief.
    sky: 'A once-bright figure, dimmed but still holding its shape low in ' +
         'the south. Recognisable, and no longer the brightest thing there.',
  }),

  reading({
    title: 'This Is Me',
    artist: 'Keala Settle',
    asOf: '2026-08-11',
    centre: 'The decision to stop hiding. Standing in full view after years ' +
            'of being told to stay small.',
    territories: [
      { mode: 'Mixolydian', dwell: DWELL.HOME,
        note: 'The open roads and crossroads. The anthemic forward drive — ' +
              'defiant, and rising.' },
      { mode: 'Ionian', dwell: DWELL.THROUGH,
        note: 'The clear daylight plains. Bright major-key declaration: the ' +
              'moment the light lands and the refusal to look away.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. A grounded human warmth that keeps the ' +
              'defiance from turning into bravado.' },
      { mode: 'Aeolian', dwell: DWELL.GLANCED,
        note: 'Brief returns to the earlier darkness, entered only in order ' +
              'to be climbed out of again.' },
    ],
    refuses: ['Phrygian', 'Locrian'],
    paths: 'Strong, outward-shooting paths that start low, climb hard toward ' +
           'the centre, and then radiate from it.',
    // This carried no motion when it was filed. MOTION.SHAPE had three
    // values and none of them was this: the centre is a *waypoint*, climbed
    // to and then gone out from. Forcing it into `departs` would have been
    // editing the observation until the instrument stopped objecting, and
    // adding a value on one example would have been legislating from a
    // single case — so the field was left off, which is what optional was
    // for, and the comment said a second example would be the evidence.
    //
    // "Firework" is that second example. RADIATES exists now, and this is
    // the first of the two readings that asked for it.
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.URGENT,
              shape: MOTION.SHAPE.RADIATES },
    sky: 'A bright figure forcing its way into view — rising rather than ' +
         'placed, and not asking whether the sky had room.',
  }),

  reading({
    title: 'Firework',
    artist: 'Katy Perry',
    asOf: '2026-08-11',
    centre: 'The spark that refuses to stay buried — the moment pressure ' +
            'turns into light.',
    territories: [
      { mode: 'Ionian', dwell: DWELL.HOME,
        note: 'The clear daylight plains. Bright major-key lift and ' +
              'declaration.' },
      { mode: 'Mixolydian', dwell: DWELL.THROUGH,
        note: 'The open roads. The driving, anthemic push that keeps the ' +
              'energy moving forward.' },
      { mode: 'Lydian', dwell: DWELL.THROUGH,
        note: 'The high bright uplands — the sparkling, slightly elevated ' +
              'quality of the chorus, like breaking through atmosphere.' },
      { mode: 'Dorian', dwell: DWELL.THROUGH,
        note: 'The rolling hills. A steady grounded warmth under the ' +
              'brightness.' },
      { mode: 'Aeolian', dwell: DWELL.GLANCED,
        note: 'The opening shadow only. The song climbs out of the night ' +
              'country and stays in the light.' },
    ],
    // Empty, and not an oversight: this reading names no refusal. The eight
    // before it all did. Phrygian and Locrian are therefore *unspoken* here
    // — questions nobody answered — rather than answered in the negative.
    //
    // The distinction earns itself immediately. These territories are
    // identical to Hey There Delilah's and Lucky's, both of which refuse
    // Phrygian and Locrian. The only thing separating this reading from
    // those two is that they spoke and this one did not. A shape that
    // treated absent-refusal and stated-refusal alike would have made three
    // readings into one.
    refuses: [],
    paths: 'Strong upward-shooting paths that start low and then explode ' +
           'outward from the centre.',
    // The second waypoint centre, and the reason RADIATES exists.
    motion: { reach: MOTION.REACH.FAR, pace: MOTION.PACE.URGENT,
              shape: MOTION.SHAPE.RADIATES },
    sky: 'A sudden flare rising in the south — the kind that makes people ' +
         'look up, and is gone before they finish deciding what it was.',
  }),
]);

/**
 * Works this atlas places identically — the resolution limit, reported.
 *
 * Reads as a statement about the vocabulary, which is only true because
 * register() has already guaranteed every entry is a distinct work. Without
 * that guarantee this function cannot tell "two songs land in the same place"
 * from "one song was filed twice", and it would report the second as the
 * first. The two live apart on purpose: one is a limit worth showing, the
 * other is an error worth stopping.
 *
 * Hey There Delilah and Lucky come out the same: Ionian home, Lydian and
 * Mixolydian and Dorian passed through, Aeolian glanced, Phrygian and
 * Locrian refused. Their wheels are the same drawing with a different name
 * on it. Both are bright major-key devotion songs that touch loneliness and
 * will not enter the dark edges, so the collision is telling the truth about
 * the vocabulary rather than about the songs.
 *
 * This is a function instead of a test that forbids collisions, and the
 * difference matters. A test would have made the atlas's own coarseness into
 * an error and pushed whoever hit it toward editing a reading until the
 * structure stopped complaining — bending the observation to fit the
 * instrument. Naming the limit lets it stay visible until either the
 * vocabulary grows a distinction that separates them, or somebody decides
 * these two really do live in the same place.
 */
export function collisions(readings = READINGS) {
  const signature = (r) => JSON.stringify([
    r.territories.map((t) => `${t.mode}:${t.dwell}`).sort(),
    [...r.refuses].sort(),
  ]);
  const grouped = new Map();
  for (const read of readings) {
    const key = signature(read);
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key).push(read.title);
  }
  return [...grouped.values()].filter((titles) => titles.length > 1);
}

/**
 * How much of the atlas's detail is structural, as a number.
 *
 * Five readings, three distinct placements. The prose tells five songs
 * apart; the structure tells three. That ratio is the honest measure of
 * what the drawn wheel can and cannot show, and it is falling as readings
 * arrive — which is information about the vocabulary, not about the songs.
 *
 * Kept as a computed figure rather than a sentence in a document because a
 * sentence would have been written once and then quietly stopped being
 * true. Same reason the reachability count in the companion repo became a
 * test: a number nobody recomputes is a number that drifts.
 */
export function resolution(readings = READINGS) {
  const place = (r) => JSON.stringify([
    r.territories.map((t) => `${t.mode}:${t.dwell}`).sort(),
    [...r.refuses].sort(),
  ]);
  const withMotion = (r) => place(r) + JSON.stringify(r.motion ?? null);

  const distinct = new Set(readings.map(place));
  const distinctWithMotion = new Set(readings.map(withMotion));
  return {
    readings: readings.length,
    distinctPlacements: distinct.size,
    indistinguishable: readings.length - distinct.size,
    // What the motion vocabulary bought. Reported rather than assumed: it
    // was added to separate the collisions, and it separated one of the two.
    distinctWithMotion: distinctWithMotion.size,
    stillIndistinguishable: readings.length - distinctWithMotion.size,
  };
}

/**
 * The edge of the surveyed part of this atlas: which territories have been
 * entered, which only refused, and which nobody has been to at all.
 *
 * Worth computing because a striking thing fell out of it. For five readings
 * Phrygian existed only as a refusal — named by everything that would not go
 * there — until a sixth entered it. That leaves **Locrian** as the sole mode
 * no work has ever entered, and Locrian is exactly the mode the interval
 * arithmetic marks as unstable: the only one with no perfect fifth to hold
 * its tonic still.
 *
 * Two independent layers agreeing without being made to. The dreamed readings
 * were written by ear, by somebody not consulting `hasPerfectFifth`.
 *
 * And the caveat, which belongs beside the observation rather than below it:
 * six readings is a small sample from one idiom. Phrygian and Locrian are rare
 * in contemporary popular song generally, so this may be a fact about the
 * genre these works come from rather than about the modes. It is offered as a
 * pattern noticed, not a law demonstrated.
 */
export function frontier(readings = READINGS) {
  const entered = new Set();
  const refused = new Set();
  for (const read of readings) {
    read.territories.forEach((t) => entered.add(t.mode));
    read.refuses.forEach((m) => refused.add(m));
  }
  const all = ['Ionian', 'Dorian', 'Phrygian', 'Lydian',
               'Mixolydian', 'Aeolian', 'Locrian'];
  return {
    entered: all.filter((m) => entered.has(m)),
    refusedOnly: all.filter((m) => refused.has(m) && !entered.has(m)),
    unvisited: all.filter((m) => !entered.has(m)),
    neverMentioned: all.filter((m) => !entered.has(m) && !refused.has(m)),
  };
}

/** Every mode any reading has placed a work in, and how often. */
export function territoryCounts(readings = READINGS) {
  const counts = new Map();
  for (const read of readings) {
    for (const t of read.territories) {
      counts.set(t.mode, (counts.get(t.mode) ?? 0) + 1);
    }
  }
  return counts;
}
