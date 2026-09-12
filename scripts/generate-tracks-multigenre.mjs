import fs from 'fs';
import path from 'path';

const __dirname = path.dirname(new URL(import.meta.url).pathname);

const GENRES = {
  'Drum & Bass': { colors: ['purple', 'orange'], bpmRange: [160, 180], remixers: 8 },
  'House': { colors: ['blue', 'cyan'], bpmRange: [120, 130], remixers: 8 },
  'Techno': { colors: ['gray', 'red'], bpmRange: [120, 135], remixers: 7 },
  'Trance': { colors: ['pink', 'purple'], bpmRange: [130, 150], remixers: 7 },
  'Ambient': { colors: ['blue', 'green'], bpmRange: [60, 90], remixers: 5 },
  'Deep House': { colors: ['teal', 'blue'], bpmRange: [110, 125], remixers: 6 },
  'Indie': { colors: ['yellow', 'orange'], bpmRange: [90, 120], remixers: 5 },
  'Hip-Hop': { colors: ['gray', 'gold'], bpmRange: [85, 105], remixers: 6 },
  'Rock': { colors: ['red', 'black'], bpmRange: [100, 140], remixers: 5 },
  'Jazz': { colors: ['gold', 'brown'], bpmRange: [80, 120], remixers: 4 },
  'Downtempo': { colors: ['green', 'teal'], bpmRange: [90, 110], remixers: 6 },
  'Dubstep': { colors: ['red', 'yellow'], bpmRange: [140, 180], remixers: 7 },
};

const AUSTRALIAN_ARTISTS = [
  'Pendulum', 'Calibre', 'High Contrast', 'The Presets', 'Cut Copy', 'Tones and I',
  'Rüfüs DU SOL', 'Bag Raiders', 'What So Not', 'Flume', 'Ta-ku', 'George Maple',
  'Peking Duk', 'Baker Boy', 'Chet Faker', 'Flight Facilities', 'Purity Ring (feat.)',
  'Stakez', 'Marky', 'S.P.Y', 'Strategy', 'Marcus Intalex', 'Calibre', 'High Contrast',
  'Logistics', 'Total Science', 'London Elektricity', 'Apex Predator', 'Chase & Status',
  'Andy C', 'Logistics', 'Hospital Records', 'BBC Recording', 'Australian Broadcasting',
  'Sydney Sound', 'Melbourne Deep', 'Brisbane Bass', 'Perth Electronic', 'Adelaide Wave',
  'Canberra Collective', 'Hobart Depth', 'Darwin Dynamics'
];

const GLOBAL_ARTISTS = [
  'Daft Punk', 'The Chemical Brothers', 'Fatboy Slim', 'Underworld', 'Leftfield',
  'Massive Attack', 'Portishead', 'Björk', 'Thom Yorke', 'Aphex Twin',
  'Boards of Canada', 'Autechre', 'Squarepusher', 'Amon Tobin', 'Tycho',
  'Jon Hopkins', 'Deadmau5', 'Calvin Harris', 'David Guetta', 'Avicii',
  'Tiësto', 'Armin van Buuren', 'Trance Fusion', 'Paul Oakenfold', 'Ferry Corsten',
  'Above & Beyond', 'Anjunadeep', 'Lane 8', 'Deadmau5', 'Eric Prydz',
  'Carl Cox', 'Adam Beyer', 'Charlotte de Witte', 'Amelie Lens', 'ANNA',
  'Amelie Lens', 'Pan-Pot', 'Ellen Allien', 'Ben Klock', 'Marcel Dettmann',
  'The Beatles', 'Led Zeppelin', 'Pink Floyd', 'The Rolling Stones', 'Queen',
  'David Bowie', 'The Who', 'Jimi Hendrix', 'Metallica', 'Black Sabbath',
  'Miles Davis', 'John Coltrane', 'Thelonius Monk', 'Dizzy Gillespie', 'Bill Evans',
  'Kanye West', 'Jay-Z', 'Nas', 'Rakim', 'KRS-One', 'Tupac', 'Biggie',
  'Radiohead', 'Arcade Fire', 'Arctic Monkeys', 'The Strokes', 'Interpol',
  'Bon Iver', 'Grimes', 'CHVRCHES', 'M83', 'Moderat'
];

const CATEGORIES = [
  'Electronic', 'Dance', 'Experimental', 'Chill', 'Energetic',
  'Dark', 'Bright', 'Atmospheric', 'Melodic', 'Percussive'
];

const YEARS = Array.from({ length: 30 }, (_, i) => 1995 + i);

const REALM_MAPPING = {
  'Drum & Bass': 'velocity',
  'Dubstep': 'velocity',
  'Techno': 'velocity',
  'House': 'flow',
  'Deep House': 'flow',
  'Trance': 'flow',
  'Ambient': 'serenity',
  'Downtempo': 'serenity',
  'Hip-Hop': 'expression',
  'Indie': 'expression',
  'Rock': 'foundation',
  'Jazz': 'dialogue'
};

function generateTrack(id, genre, artistList, genre_config) {
  const isAustralian = Math.random() < 0.25;
  const artists = isAustralian ? AUSTRALIAN_ARTISTS : GLOBAL_ARTISTS;
  const artist = artists[Math.floor(Math.random() * artists.length)];
  const remixer = Math.random() < 0.3 ? artists[Math.floor(Math.random() * artists.length)] : null;

  const year = YEARS[Math.floor(Math.random() * YEARS.length)];
  const [bpmMin, bpmMax] = genre_config.bpmRange;
  const bpm = Math.floor(Math.random() * (bpmMax - bpmMin + 1)) + bpmMin;

  const keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const key = keys[Math.floor(Math.random() * keys.length)];
  const keyMinor = Math.random() < 0.3;

  const duration = Math.floor(Math.random() * (480 - 180)) + 180;
  const category = CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)];

  const genreArray = [genre];
  if (Math.random() < 0.2) {
    const otherGenres = Object.keys(GENRES).filter(g => g !== genre);
    genreArray.push(otherGenres[Math.floor(Math.random() * otherGenres.length)]);
  }

  const realm = isAustralian ? 'horizon' : REALM_MAPPING[genre];

  return {
    id: `track_${String(id).padStart(5, '0')}`,
    title: `${artist} - ${genre} Track ${id}`,
    artist: artist,
    remixer: remixer,
    year: year,
    duration: duration,
    bpm: bpm,
    key: key + (keyMinor ? 'm' : ''),
    category: category,
    genres: genreArray,
    sourceUrl: `https://example.com/track/${id}`,
    releaseDate: `${year}-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
    label: isAustralian ? 'Australian Records' : `${genre} Label`,
    isRemix: !!remixer,
    remixChainId: remixer ? `remix_chain_${id}` : null,
    featured: Math.random() < 0.1,
    isAustralian: isAustralian,
    realm: realm
  };
}

console.log('Generating 2,500 tracks across 12 genres...');

const tracks = [];
let trackId = 1;

for (const [genre, config] of Object.entries(GENRES)) {
  const tracksPerGenre = Math.floor(2500 / Object.keys(GENRES).length);
  console.log(`  ${genre}: ${tracksPerGenre} tracks`);

  for (let i = 0; i < tracksPerGenre; i++) {
    tracks.push(generateTrack(trackId++, genre, AUSTRALIAN_ARTISTS, config));
  }
}

console.log(`Generated ${tracks.length} total tracks`);

// Generate indexes
const indexes = {
  artists: [...new Set(tracks.map(t => t.artist))].sort(),
  years: [...new Set(tracks.map(t => t.year))].sort((a, b) => a - b),
  categories: [...new Set(tracks.flatMap(t => [t.category]))].sort(),
  genres: Object.keys(GENRES).sort(),
  remixers: [...new Set(tracks.filter(t => t.remixer).map(t => t.remixer))].sort(),
  labels: [...new Set(tracks.map(t => t.label))].sort(),
  keys: [...new Set(tracks.map(t => t.key))].sort(),
  realms: [...new Set(tracks.map(t => t.realm))].sort(),
  bpmRanges: [
    { min: 60, max: 90, label: 'Slow' },
    { min: 90, max: 120, label: 'Medium' },
    { min: 120, max: 140, label: 'Fast' },
    { min: 140, max: 160, label: 'Very Fast' },
    { min: 160, max: 180, label: 'Intense' },
    { min: 180, max: 200, label: 'Extreme' }
  ],
  australianArtists: [...new Set(tracks.filter(t => t.isAustralian).map(t => t.artist))].sort()
};

console.log(`Artists: ${indexes.artists.length}`);
console.log(`Years: ${indexes.years.length}`);
console.log(`Genres: ${indexes.genres.length}`);
console.log(`Realms: ${indexes.realms.length}`);
console.log(`Australian Artists: ${indexes.australianArtists.length}`);

// Write to files
const srcDir = path.join(__dirname, '..', 'src', 'data');
const publicDir = path.join(__dirname, '..', 'public', 'data');

[srcDir, publicDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(path.join(dir, 'tracks.json'), JSON.stringify(tracks, null, 2));
  fs.writeFileSync(path.join(dir, 'indexes.json'), JSON.stringify(indexes, null, 2));
  console.log(`Written to ${dir}`);
});

console.log('✓ Multi-genre track database generated successfully');
