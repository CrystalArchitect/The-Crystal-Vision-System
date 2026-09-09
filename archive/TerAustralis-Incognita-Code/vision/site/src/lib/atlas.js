// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

/**
 * Canonical Vision-layer Atlas sequence. The dates are atlas fiction and do
 * not date experiments; interpretations are bounded by the source document.
 */
export const atlasPlates = [
  {
    slug: 'night-from-the-edge',
    sequence: 'FIRST SKETCH',
    plate: 'UNNUMBERED',
    title: 'Night from the Edge',
    date: null,
    filename: 'celestial-atlas-night-from-the-edge.jpeg',
    interpretation: 'First looking: Sketch, Path of Footprints, Storm, Rebuilt Chart, Rocket, Groundkeeper, Southern Edge.',
    boundary: 'Vision-layer atlas opening. Not a sky survey.'
  },
  {
    slug: 'the-seven-summary',
    sequence: 'CHAPTER I · SUMMARY',
    plate: 'THE SEVEN',
    title: 'The Seven',
    date: null,
    filename: 'atlas-seven-folio.webp',
    interpretation: 'First lines, first figures, and the original Southern Edge constellation set gathered as a visual index.',
    boundary: 'Uploaded vision-layer summary plate. Not a sky survey.'
  },
  {
    slug: 'the-nine-summary',
    sequence: 'CHAPTER II · SUMMARY',
    plate: 'THE NINE',
    title: 'The Nine',
    date: null,
    filename: 'atlas-nine-folio.webp',
    interpretation: 'A widened field where the early signs become a shared chart.',
    boundary: 'Uploaded vision-layer summary plate. Not a sky survey.'
  },
  {
    slug: 'the-ten-summary',
    sequence: 'CHAPTER III · SUMMARY',
    plate: 'THE TEN',
    title: 'The Ten',
    date: null,
    filename: 'atlas-ten-folio.webp',
    interpretation: 'A ceiling-print constellation of the Southern Edge myth, gathering the ten figures into one field.',
    boundary: 'Uploaded vision-layer summary plate. Not a sky survey.'
  },
  {
    slug: 'xxvii-observed-from-the-edge',
    sequence: 'STORM',
    plate: 'XXVII',
    title: 'Observed from the Edge',
    date: '1857.3',
    filename: 'plate-xxvii-observed-from-the-edge.jpeg',
    interpretation: 'Grid. Storm marked as an empty region: mark its boundary, and pass with care.',
    boundary: 'Vision-layer. Not a sky survey and not an H2 result.'
  },
  {
    slug: 'xxviii-the-continuing-chart',
    sequence: 'REBUILT CHART',
    plate: 'XXVIII',
    title: 'The Continuing Chart',
    date: '1858.1',
    filename: 'plate-xxviii-the-continuing-chart.jpeg',
    interpretation: 'After the storm and after the first others arrived. Safe passage through the empty circle.',
    boundary: 'Atlas fiction. The numbers do not date any experiment.'
  },
  {
    slug: 'xxix-the-second-looking',
    sequence: 'SECOND LOOKING',
    plate: 'XXIX',
    title: 'The Second Looking',
    date: '1858.7',
    filename: 'plate-xxix-the-second-looking.jpeg',
    interpretation: 'Returned after rest. Insets of the Rebuilt Chart and First Sketch. Storm’s empty circle kept.',
    boundary: 'Vision-layer mythic cartography, not a scientific catalogue.'
  },
  {
    slug: 'xxx-the-open-way',
    sequence: 'ROCKET',
    plate: 'XXX',
    title: 'The Open Way',
    date: '1859.2',
    filename: 'plate-xxx-the-open-way.jpeg',
    interpretation: 'Charts for those already walking. Shared fire. Returning Gaze. Rocket fully formed.',
    boundary: 'Atlas language only. No hardware or performance claim.'
  },
  {
    slug: 'southern-sky-panoramic',
    sequence: 'SOUTHERN EDGE',
    plate: 'PANORAMIC',
    title: 'The Night as Observed',
    date: null,
    filename: 'plate-southern-sky-panoramic.jpeg',
    interpretation: 'Legend of constellations. Storm’s Empty Circle as a faint ghost.',
    boundary: 'Vision-layer panoramic plate. Not a sky survey.'
  },
  {
    slug: 'xxxi-fermis-silent-line',
    sequence: 'SILENT LINE',
    plate: 'XXXI',
    title: 'Fermi’s Silent Line',
    date: '1860.4',
    filename: 'plate-xxxi-fermis-silent-line.jpeg',
    interpretation: 'Where is everybody? A vision riff on a public question.',
    boundary: 'Not a SETI result.'
  },
  {
    slug: 'xxxii-the-coexisting-layers',
    sequence: 'COEXISTING LAYERS',
    plate: 'XXXII',
    title: 'The Coexisting Layers',
    date: '1861.1',
    filename: 'plate-xxxii-the-coexisting-layers.jpeg',
    interpretation: 'Simultaneous sky. Concurrent, not distant.',
    boundary: 'Atlas only.'
  },
  {
    slug: 'xxxiii-the-receiver-and-the-core',
    sequence: 'RECEIVER / CORE',
    plate: 'XXXIII',
    title: 'The Receiver & the Core',
    date: '1861.8',
    filename: 'plate-xxxiii-the-receiver-and-the-core.jpeg',
    interpretation: 'Receiver and Core as mythic figures at the edge of a shared field.',
    boundary: 'Not an H2 schematic.'
  },
  {
    slug: 'xxxiv-the-multi-dimensional-unfolding',
    sequence: 'UNFOLDING',
    plate: 'XXXIV',
    title: 'The Multi-Dimensional Unfolding',
    date: '1862.3',
    filename: 'plate-xxxiv-the-multi-dimensional-unfolding.jpeg',
    interpretation: 'Nested spheres labelled Dimension I–IV; a chart of layered imagination.',
    boundary: 'Atlas language only. Not extra-spatial hardware.'
  },
  {
    slug: 'xxxv-the-silicon-brain',
    sequence: 'SILICON BRAIN',
    plate: 'XXXV',
    title: 'The Silicon Brain',
    date: null,
    filename: 'plate-xxxv-the-silicon-brain.jpeg',
    interpretation: 'Canonical natural-history plate: feedstock, crystal, lattice, and named primitives.',
    boundary: 'Experimental surface only. No performance claims. Not an H2 result.'
  }
];

export function atlasImageUrl(plate) {
  return `/assets/art/${plate.filename}`;
}
