export type Badge =
  | "LIVE"
  | "MERGED"
  | "CANON"
  | "HELD"
  | "EXTERNAL"
  | "CORRECTED";

export type Ring = "core" | "lattice" | "starline" | "horizon" | "external";

export type EdgeKind = "runtime" | "authoring" | "grounding" | "boundary";

export type MapNode = {
  id: string;
  label: string;
  short: string;
  ring: Ring;
  badge: Badge;
  note: string;
  source?: string;
  x: number;
  y: number;
};

export type MapEdge = {
  from: string;
  to: string;
  kind: EdgeKind;
};

export const MAP_NODES: MapNode[] = [
  {
    id: "CC",
    label: "CrystalCore",
    short: "CC",
    ring: "core",
    badge: "LIVE",
    note: "Local-first OS surface. Consent is a runtime property.",
    source: "crystalcore / five-door gate",
    x: 180,
    y: 198,
  },
  {
    id: "OP",
    label: "Operator",
    short: "OP",
    ring: "core",
    badge: "CANON",
    note: "Human at the gate. Latest revoke or reinstate wins.",
    x: 180,
    y: 142,
  },
  {
    id: "GATE",
    label: "Consent gate",
    short: "GATE",
    ring: "lattice",
    badge: "MERGED",
    note: "Five doors: revocation, approval, provenance, permission, scope.",
    source: "gate.py · fail-closed",
    x: 92,
    y: 168,
  },
  {
    id: "MEM",
    label: "Memory layers",
    short: "MEM",
    ring: "lattice",
    badge: "MERGED",
    note: "Episodic / semantic / reflective. Working conversation is never guest-readable.",
    source: "documented taxonomy only",
    x: 268,
    y: 168,
  },
  {
    id: "BRIDGE",
    label: "CrystalBridge",
    short: "BRG",
    ring: "lattice",
    badge: "MERGED",
    note: "Guest surface. Observable ask is logged before reply.",
    source: "pending.jsonl · PRs #70 / #71",
    x: 92,
    y: 234,
  },
  {
    id: "AUDIT",
    label: "Audit ledger",
    short: "AUD",
    ring: "lattice",
    badge: "MERGED",
    note: "Revocations append-only. Corrupt ledger refuses all guests.",
    source: "revocations.jsonl",
    x: 268,
    y: 234,
  },
  {
    id: "CARD",
    label: "Operator Card",
    short: "CARD",
    ring: "lattice",
    badge: "HELD",
    note: "This preview is not a repo surface. No Operator Card exists in the public portfolio.",
    x: 180,
    y: 308,
  },
  {
    id: "TA",
    label: "TerAustralis",
    short: "TA",
    ring: "starline",
    badge: "CANON",
    note: "Australian multiplanetary vision. Business and policy track.",
    x: 52,
    y: 96,
  },
  {
    id: "SAT",
    label: "Synthetic Affect",
    short: "SAT",
    ring: "starline",
    badge: "CANON",
    note: "Project-originated theory name. Neighbour fields exist; this is not a prior academic school.",
    source: "CrystalCore.OS /synthetic-affect",
    x: 308,
    y: 96,
  },
  {
    id: "MYTHOS",
    label: "Mythos",
    short: "MYTH",
    ring: "starline",
    badge: "CANON",
    note: "Story layer. Labelled Story, not Science.",
    x: 180,
    y: 64,
  },
  {
    id: "LOGOS",
    label: "Logos",
    short: "LOG",
    ring: "starline",
    badge: "CANON",
    note: "Spec and tests. Labelled Science when measured.",
    x: 308,
    y: 308,
  },
  {
    id: "STARLINE",
    label: "Starline",
    short: "STL",
    ring: "starline",
    badge: "CORRECTED",
    note: "Wire-protocol fragment kinds exist in consent_transport. Earlier ‘unimplemented’ claim was false.",
    source: "fragment.py KINDS",
    x: 52,
    y: 308,
  },
  {
    id: "COUNTRY",
    label: "Country",
    short: "CTY",
    ring: "horizon",
    badge: "CANON",
    note: "Honour Country. Homage, not ownership. No Songline claimed as IP.",
    x: 88,
    y: 372,
  },
  {
    id: "FAMILY",
    label: "Ordinary life",
    short: "LIFE",
    ring: "horizon",
    badge: "CANON",
    note: "Family, rest, housing, and safety outrank every terminal command.",
    x: 180,
    y: 392,
  },
  {
    id: "PUBLIC",
    label: "Public node",
    short: "PUB",
    ring: "horizon",
    badge: "HELD",
    note: "Published surfaces must stay world-safe. This preview is not the public repo node.",
    x: 272,
    y: 372,
  },
  {
    id: "EXT",
    label: "Named externals",
    short: "EXT",
    ring: "external",
    badge: "EXTERNAL",
    note: "xAI / Grok / Tesla / Neuralink — named, not claimed.",
    x: 328,
    y: 36,
  },
  {
    id: "NET",
    label: "Public net",
    short: "NET",
    ring: "external",
    badge: "EXTERNAL",
    note: "Outside the lattice. No implied partnership or access.",
    x: 32,
    y: 36,
  },
];

export const MAP_EDGES: MapEdge[] = [
  { from: "OP", to: "CC", kind: "runtime" },
  { from: "CC", to: "GATE", kind: "runtime" },
  { from: "CC", to: "MEM", kind: "runtime" },
  { from: "CC", to: "BRIDGE", kind: "runtime" },
  { from: "CC", to: "AUDIT", kind: "runtime" },
  { from: "GATE", to: "CARD", kind: "authoring" },
  { from: "CC", to: "TA", kind: "authoring" },
  { from: "CC", to: "SAT", kind: "authoring" },
  { from: "CC", to: "STARLINE", kind: "authoring" },
  { from: "MYTHOS", to: "LOGOS", kind: "authoring" },
  { from: "MYTHOS", to: "CC", kind: "authoring" },
  { from: "OP", to: "FAMILY", kind: "grounding" },
  { from: "CC", to: "COUNTRY", kind: "grounding" },
  { from: "CC", to: "PUBLIC", kind: "authoring" },
  { from: "EXT", to: "NET", kind: "boundary" },
  { from: "NET", to: "CC", kind: "boundary" },
];

export const DOORS = [
  { id: "revocation", label: "Revocation", detail: "Latest human revoke or reinstate wins." },
  { id: "approval", label: "Approval", detail: "Standing grant is present." },
  { id: "provenance", label: "Provenance", detail: "Token proves the guest." },
  { id: "permission", label: "Permission", detail: "Tool is on the grant list." },
  { id: "scope", label: "Scope", detail: "read/write and memory types granted." },
] as const;

export const FLOW = [
  { id: "baseline", label: "Baseline check", kind: "real" as const, detail: "Status only. Changes nothing." },
  { id: "one", label: "One command", kind: "real" as const, detail: "Render, ledger, scan, or gate status." },
  { id: "life", label: "Ordinary life", kind: "real" as const, detail: "Family and rest outrank the terminal." },
  { id: "hold", label: "Hold / stand down", kind: "real" as const, detail: "Always available. Returns to idle." },
  { id: "card", label: "Operator Card app", kind: "designed" as const, detail: "Preview only. Not in the public repos." },
] as const;

export const OWNERSHIP = {
  ours: [
    "CrystalCore OS",
    "CrystalBridge",
    "TerAustralis Incognita",
    "This operator preview",
    "Synthetic Affect Theory (project name)",
  ],
  notOurs: [
    "Third-party unit papers and labels",
    "xAI / Grok / Tesla / Neuralink (named, not claimed)",
    "Country / Songline knowledge (homage, not ownership)",
  ],
};
