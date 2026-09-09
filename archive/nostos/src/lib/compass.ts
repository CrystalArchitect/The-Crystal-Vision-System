export const compassFile = {
  id: "BUILT-COMPASS",
  title: "Star compass",
  subtitle: "Thirty-two houses · a bearing, not an appointment",
  stamp: "A house is a width of ocean. Stars do not choose you.",
  footer: "Hawaiian teaching compass. Country first. Do not flatten this onto the south.",
  source: "Nainoa Thompson / Hōkūleʻa, from Mau Piailug’s construct, Hawaiian names.",
} as const;

export const definition = {
  kicker: "Built",
  title: "Not a device",
  body: "A house is the place a star, sun, moon, or planet comes out of the ocean and goes back in. The Hawaiian teaching compass is a mental 32-point circle. 11.25° each. 360°. It is not brass. It is not Polaris-in-a-box. Near the equator you steer by rise and set.",
};

export const cardinals = [
  { name: "Hikina", job: "East — arriving horizon" },
  { name: "Komohana", job: "West — entering horizon" },
  { name: "ʻĀkau", job: "North (right, if you face west)" },
  { name: "Hema", job: "South (left)" },
] as const;

export const quadrants = [
  { name: "Koʻolau", job: "Northeast" },
  { name: "Malanai", job: "Southeast" },
  { name: "Kona", job: "Southwest" },
  { name: "Hoʻolua", job: "Northwest" },
] as const;

export const houses = [
  { name: "Lā", meaning: "Sun", role: "Closest to east/west. Where the sun rises and sets most of the year." },
  { name: "ʻĀina", meaning: "Land", role: "Belt where Hawaiʻi (~21°N) and Tahiti (~18°S) sit relative to the equator." },
  { name: "Noio", meaning: "Noddy tern", role: "Living compass: fishes out at dawn, returns to land at dusk." },
  { name: "Manu", meaning: "Bird", role: "Midway between cardinals. Canoe as bird." },
  { name: "Nālani", meaning: "Heavens", role: "Further round toward north/south." },
  { name: "Nāleo", meaning: "Voices", role: "Stars as bearings that speak." },
  { name: "Haka", meaning: "Empty", role: "Closest to north/south. Spare house." },
] as const;

export const rule = {
  title: "The one rule",
  body: "A star that rises in a house on the east sets in the house of the same name on the west. Rise in ʻĀina Koʻolau → arc over → set in ʻĀina Hoʻolua. It does not wander into a new house. Parallel tracks. Hemisphere stays hemisphere.",
};

export const steer = [
  "Name the course as a house, not as 045°.",
  "Wait for a star that lives in that house at the horizon.",
  "When it climbs too high, switch to the next star in the same house. That sequence is the route.",
  "Day: sun in Lā. Sun too high: swell. Night gone: Noio, wind, colour of water.",
] as const;

export const notThis = [
  "Not every Polynesian island using these 32 Hawaiian names. This is the Hōkūleʻa teaching compass. Mau’s Micronesian pointing is the root.",
  "Not Homeric kit. Calypso: Bear on the left, sail east. One circumpolar. Coarser grain. Different sky.",
  "Not Crux-as-throne. Southern Cross finds south as a constructed pole. A house finds any heading as a rise/set pair.",
  "Not to be flattened onto Country here. Do not appoint the Cross. Do not import a Hawaiian house as an Australian claim.",
] as const;

export const southern = {
  title: "If you put Crux in a house",
  body: "Treat its rise as one star in a southern Haka or Nālani queue. That is a starline in the Built sense: a memorised house sequence. It is not a myth that the Cross appointed the navigator. Heading is a night skill. Recovery is still a job.",
};
