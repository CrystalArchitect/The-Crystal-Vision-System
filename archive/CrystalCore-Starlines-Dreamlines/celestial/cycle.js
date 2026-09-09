/**
 * The cycle chart — after Connie Kaplan's Dream Chart.
 *
 * The attribution is the first thing in this file, before the code and before
 * any data, because that is the condition under which this was built. A credit
 * a reader has to go looking for is a quiet version of the absorption being
 * refused — and implementing a structure while dropping the name removes the
 * acknowledgment, not the borrowing.
 *
 * **The book is confirmed, from the object.**
 *
 *   Connie Cockrell Kaplan, *The Woman's Book of Dreams: Dreaming as a
 *   Spiritual Practice*, foreword by Jamie Sams.
 *
 * Read off a photograph of the cover, held by the person who also photographed
 * page 63: the *Dream Chart*, a twenty-nine-spoke wheel filled in by hand with
 * a blank template facing it, Name field *Connie Kaplan*, dates 29 December
 * 1994 to 26 January 1995, captioned "(29-day cycle)".
 *
 * An earlier version of this file named this book on the strength of a search
 * match, with the inferential step removed — the precise error PRECEDENTS.md
 * records against a modern book's Apian caption. The guess turned out right,
 * which changes nothing about it having been a guess presented as a fact. It
 * is a fact now because somebody went and looked.
 *
 * The copyright page then corrected the one field that had been marked as
 * weaker than the rest. The ISBN carried here from catalogue records was
 * **1-58270-008-7** — the Beyond Words printing. The copy the chart was
 * photographed from is a different one: *This Edition Printed For Axiom
 * Publishing, 2000*, ISBN **1-86476-056-7**. Both are real; they are not the
 * same book in hand.
 *
 * That is the whole argument for splitting a citation by how each part is
 * known. The field flagged as not-from-the-object was the field that was
 * wrong, and it was wrong in the quietest possible way: a correct ISBN for a
 * different printing, which no amount of re-reading the sentence would catch.
 *
 * One assumption remains, unchanged by any of the three photographs: that the
 * page 63 photograph, the cover and the copyright page are the same copy. That
 * is the ordinary reading and not a proof.
 *
 * What is hers: the form. Days of a lunar cycle around a wheel, one wedge each,
 * what was dreamt or what happened written into the wedge, and empty days
 * *written in* as void rather than left blank.
 *
 * What is this project's: the code, and the refusals below.
 *
 * This is a different atlas from the mode wheel next door — days around a
 * cycle, not works around a tonal ring — and neither subsumes the other. It is
 * here because it independently arrived at a distinction this layer had to
 * argue itself into: **a marked absence is a reading; an unmarked one is
 * silence.** Somebody doing this by hand in 1995 wrote the void in rather than
 * skipping the wedge, for the same reason `refuses` exists.
 *
 * It holds no days. The entries would be somebody's dreams, and this file has
 * none — it draws its own emptiness the way the sky layer did while no
 * catalogue was reachable.
 */

import { BELT } from './atlas.js';

/**
 * Named exactly once, and carried onto the drawing itself.
 *
 * It credits the person and the form, and stops short of the edition, because
 * the edition is not established. A citation that names a book it has not
 * confirmed is worse than one that names the author and admits the gap: the
 * first looks finished and cannot be questioned, the second invites the
 * correction that would finish it.
 */
export const AFTER =
  "after Connie Cockrell Kaplan's Dream Chart — The Woman's Book of Dreams: " +
  'Dreaming as a Spiritual Practice (© 1999; Axiom Publishing, 2000)';

/**
 * The citation, with each part carrying where it came from.
 *
 * Split this way because "confirmed" is not one state. The book is confirmed
 * from a photograph of its cover; the imprint details are not — they are
 * catalogue records, which are usually right and are not the object. Flatten
 * the two and the weaker half inherits the strength of the better half, which
 * is how a provenance quietly goes missing.
 */
export const CITATION = Object.freeze({
  author: 'Connie Cockrell Kaplan',
  title: "The Woman's Book of Dreams: Dreaming as a Spiritual Practice",
  foreword: 'Jamie Sams',
  form: 'Dream Chart — a 29-day cycle wheel, one wedge per day',
  /** All of it read directly off photographs of the book itself. */
  fromTheObject: Object.freeze([
    'author', 'title', 'foreword', 'form',
    'copyright', 'originalPublisher', 'edition', 'isbn', 'lccn',
  ]),
  copyright: '\u00a9 1999 by Connie Cockrell Kaplan',
  originalPublisher: 'Beyond Words Publishing, Inc., Hillsboro, Oregon',
  edition: 'This edition printed for Axiom Publishing, 2000',
  isbn: '1-86476-056-7 (pbk.)',
  lccn: "98-50197 \u00b7 BF1099.W65K36 1999 \u00b7 135'.3\u2014dc21",
  /**
   * What the catalogue records had said, kept as the correction it turned out
   * to be rather than deleted. 1-58270-008-7 is the Beyond Words printing — a
   * real ISBN, for a different book than the one in hand. This is the whole
   * argument for splitting a citation by how each part is known: the field
   * marked weaker was the field that was wrong, and it was wrong in the
   * quietest way available.
   */
  supersededByTheObject: Object.freeze({
    isbn: '1-58270-008-7', note: 'Beyond Words printing, not this copy',
  }),
  /** The ordinary reading of three photographs, not a proof. */
  assumed: 'that the page 63, cover and copyright-page photographs are the ' +
           'same copy of the same book',
  confirmed: true,
});

/** The photographed chart runs twenty-nine wedges, and says so on its face. */
export const CYCLE_DAYS = 29;

/**
 * What a day can be, and the three are not two.
 *
 * `blank` and `void` look identical on a chart that only records presence, and
 * they are opposites: one is a day nobody wrote about, the other is a day
 * somebody looked at and marked empty. Collapsing them loses the observation
 * and keeps the gap.
 */
export const MARK = Object.freeze({
  /** Something was dreamt or happened, and it is written. */
  RECORDED: 'recorded',
  /** Looked at, and deliberately marked empty. An answer. */
  VOID: 'void',
  /** Nothing written. A question nobody has answered. */
  BLANK: 'blank',
});

/**
 * One wedge.
 *
 * A recorded day must actually say something — a day marked `recorded` with
 * no text is the failure this vocabulary exists to prevent, wearing the label
 * of the thing it is not.
 */
export function day({ number, date = '', mark = MARK.BLANK, note = '' }) {
  if (!Number.isInteger(number) || number < 1 || number > CYCLE_DAYS) {
    throw new Error(`a day runs 1–${CYCLE_DAYS}, not ${number}`);
  }
  if (!Object.values(MARK).includes(mark)) {
    throw new Error(
      `day ${number} is marked ${JSON.stringify(mark)} — use ` +
      `${Object.values(MARK).join(', ')}`);
  }
  if (mark === MARK.RECORDED && !note) {
    throw new Error(
      `day ${number} is marked recorded but says nothing. An empty recorded ` +
      `day is indistinguishable afterwards from a day nobody wrote about, ` +
      `which is the difference this chart exists to keep.`);
  }
  if (mark !== MARK.RECORDED && note) {
    throw new Error(
      `day ${number} is marked ${mark} and carries a note. If something was ` +
      `written it was recorded; if it was empty it needs no note.`);
  }
  return Object.freeze({ belt: BELT.DREAMED, number, date, mark, note });
}

/**
 * A cycle: twenty-nine days, each one present whether or not anything is in it.
 *
 * Every wedge exists from the start — a chart that grew a day only when
 * somebody wrote in it could not show the shape of a quiet month, and the
 * shape of a quiet month is a reading.
 */
export function cycle({ name = '', beginning = '', closing = '', days = [] } = {}) {
  const seen = new Map();
  for (const d of days) {
    if (seen.has(d.number)) throw new Error(`day ${d.number} appears twice`);
    seen.set(d.number, d);
  }
  const full = Array.from({ length: CYCLE_DAYS }, (_, i) =>
    seen.get(i + 1) ?? day({ number: i + 1 }));
  return Object.freeze({
    belt: BELT.DREAMED, after: AFTER,
    name, beginning, closing, days: Object.freeze(full),
  });
}

/** What a cycle presently holds, reported rather than left to be inferred. */
export function tally(c) {
  const count = (mark) => c.days.filter((d) => d.mark === mark).length;
  return {
    days: c.days.length,
    recorded: count(MARK.RECORDED),
    void: count(MARK.VOID),
    blank: count(MARK.BLANK),
  };
}

/**
 * The chart, drawn.
 *
 * Twenty-nine wedges from a centre, day one at the top, clockwise. The three
 * marks are drawn differently on purpose: a void day is *struck*, a blank day
 * is left open, and the legend says which is which. Rendering them alike would
 * undo the only reason this shape was worth building.
 *
 * The attribution is on the face of the drawing, not in a caption. A diagram
 * travels further than the file it came from and arrives without context — the
 * same argument as the belt notice on the mode wheel, and the same reason
 * `star()` demands an epoch.
 */
export function drawCycle(c, { size = 560 } = {}) {
  const mid = size / 2;
  const outer = size * 0.34;
  const inner = size * 0.11;
  const step = 360 / CYCLE_DAYS;
  const at = (deg, r) => {
    const rad = ((deg - 90) * Math.PI) / 180;
    return [mid + Math.cos(rad) * r, mid + Math.sin(rad) * r];
  };

  const wedges = c.days.map((d) => {
    const from = (d.number - 1) * step;
    const to = d.number * step;
    const [x1, y1] = at(from, inner);
    const [x2, y2] = at(from, outer);
    const [lx, ly] = at(from + step / 2, outer + 14);
    const [sx, sy] = at(from + step / 2, (inner + outer) / 2);
    return `<g class="day ${d.mark}">` +
      `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" ` +
      `x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" class="spoke" />` +
      `<text class="num" x="${lx.toFixed(1)}" y="${ly.toFixed(1)}">${d.number}</text>` +
      (d.mark === MARK.VOID
        ? `<path class="struck" transform="translate(${sx.toFixed(1)},${sy.toFixed(1)})" ` +
          `d="M-4,-4 L4,4 M4,-4 L-4,4" />`
        : '') +
      (d.mark === MARK.RECORDED
        ? `<circle class="dot" cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="3.5" />`
        : '') +
      `</g>`;
  });

  const t = tally(c);
  return `<svg viewBox="0 0 ${size} ${size}" class="cycle" role="img"
     aria-label="${CYCLE_DAYS}-day cycle chart, ${AFTER}">
  <title>${c.name || 'Cycle chart'}</title>
  <desc>${AFTER}. ${t.recorded} days recorded, ${t.void} marked void,
    ${t.blank} blank. A blank day is one nobody wrote about; a void day is one
    somebody looked at and marked empty.</desc>
  <text class="credit" x="${mid}" y="20">${AFTER.split(' — ')[0]}</text>
  <circle class="rim" cx="${mid}" cy="${mid}" r="${outer}" />
  <circle class="hub" cx="${mid}" cy="${mid}" r="${inner}" />
  ${wedges.join('\n  ')}
  <text class="belt" x="${mid}" y="${size - 12}">dreamed line — a record of dreaming, not of the sky</text>
</svg>`;
}

/** What the panel says while the chart holds nothing. */
export function cycleNotice(c) {
  const t = tally(c);
  return t.recorded === 0 && t.void === 0
    ? `${t.days} days, none of them written in. The wedges are all here ` +
      `because the shape of an empty cycle is itself a reading — and these ` +
      `entries would be somebody's dreams, which this file does not have.`
    : `${t.days} days: ${t.recorded} recorded, ${t.void} marked void, ` +
      `${t.blank} still blank.`;
}
