import { useCallback, useId, useMemo, useState } from "react";
import { X } from "lucide-react";
import {
  DOORS,
  FLOW,
  MAP_EDGES,
  MAP_NODES,
  OWNERSHIP,
  type Badge,
  type MapNode,
} from "@/lib/map-data";

type Panel = "lattice" | "doors" | "flow" | "ownership";

const BADGE_CLASS: Record<Badge, string> = {
  LIVE: "bg-ok-bg text-ok ring-ok/35",
  MERGED: "bg-info-bg text-info ring-info/30",
  CANON: "bg-surface-2 text-accent-soft ring-accent/30",
  HELD: "bg-surface-3 text-muted ring-border",
  EXTERNAL: "bg-surface text-faint ring-border",
  CORRECTED: "bg-danger-bg text-accent-soft ring-accent/40",
};

const EDGE_STROKE: Record<string, string> = {
  runtime: "var(--color-info)",
  authoring: "var(--color-accent)",
  grounding: "var(--color-ok)",
  boundary: "var(--color-faint)",
};

function nodeById(id: string) {
  return MAP_NODES.find((n) => n.id === id);
}

export function LatticeSuite() {
  const [panel, setPanel] = useState<Panel>("lattice");
  const [open, setOpen] = useState<MapNode | null>(null);

  return (
    <div className="space-y-4">
      <div className="rounded-xl bg-dust/25 px-4 py-3 ring-1 ring-dust">
        <p className="font-mono text-xs uppercase tracking-wider text-accent">Honesty</p>
        <p className="mt-1 text-sm text-muted">
          Designed map. Not live metering. Homage, not ownership. CARD is HELD — this preview
          is not a published repo surface.
        </p>
      </div>

      <div className="flex gap-1 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {(
          [
            ["lattice", "Lattice"],
            ["doors", "Five doors"],
            ["flow", "Operator flow"],
            ["ownership", "Ownership"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            onClick={() => {
              setPanel(id);
              setOpen(null);
            }}
            className={`min-h-11 shrink-0 rounded-full px-4 text-sm font-medium ring-1 transition ${
              panel === id
                ? "bg-accent text-bg ring-accent"
                : "bg-surface text-muted ring-border hover:bg-surface-2 hover:text-fg"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {panel === "lattice" ? <LatticeCanvas open={open} onOpen={setOpen} /> : null}
      {panel === "doors" ? <DoorsPanel /> : null}
      {panel === "flow" ? <FlowPanel /> : null}
      {panel === "ownership" ? <OwnershipPanel /> : null}
    </div>
  );
}

function LatticeCanvas({
  open,
  onOpen,
}: {
  open: MapNode | null;
  onOpen: (n: MapNode | null) => void;
}) {
  const gid = useId();
  const nodes = MAP_NODES;
  const byId = useMemo(() => new Map(nodes.map((n) => [n.id, n])), [nodes]);

  const select = useCallback(
    (id: string) => {
      const n = byId.get(id);
      if (n) onOpen(n);
    },
    [byId, onOpen],
  );

  return (
    <div className="relative">
      <div className="overflow-hidden rounded-xl bg-surface ring-1 ring-border">
        <svg
          viewBox="0 0 360 430"
          className="h-auto w-full"
          role="img"
          aria-label="Lattice and Starline map"
        >
          <defs>
            <radialGradient id={`${gid}-glow`} cx="50%" cy="48%" r="42%">
              <stop offset="0%" stopColor="var(--color-dust)" stopOpacity="0.45" />
              <stop offset="100%" stopColor="transparent" />
            </radialGradient>
          </defs>
          <rect width="360" height="430" fill="var(--color-surface)" />
          <circle cx="180" cy="200" r="150" fill={`url(#${gid}-glow)`} />

          {MAP_EDGES.map((e) => {
            const a = byId.get(e.from);
            const b = byId.get(e.to);
            if (!a || !b) return null;
            const dashed = e.kind === "authoring" || e.kind === "boundary";
            return (
              <line
                key={`${e.from}-${e.to}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke={EDGE_STROKE[e.kind]}
                strokeWidth={e.kind === "runtime" ? 1.6 : 1.15}
                strokeOpacity={0.55}
                strokeDasharray={dashed ? "4 3" : undefined}
              />
            );
          })}

          {nodes.map((n) => {
            const active = open?.id === n.id;
            const r = n.ring === "core" ? 22 : n.ring === "external" ? 14 : 18;
            return (
              <g
                key={n.id}
                transform={`translate(${n.x} ${n.y})`}
                tabIndex={0}
                role="button"
                aria-label={`${n.label}, ${n.badge}`}
                className="cursor-pointer outline-none"
                onClick={() => select(n.id)}
                onKeyDown={(ev) => {
                  if (ev.key === "Enter" || ev.key === " ") {
                    ev.preventDefault();
                    select(n.id);
                  }
                }}
              >
                <circle
                  r={r + (active ? 3 : 0)}
                  fill={n.ring === "core" ? "var(--color-surface-3)" : "var(--color-surface-2)"}
                  stroke={active ? "var(--color-accent-soft)" : "var(--color-border)"}
                  strokeWidth={active ? 2 : 1}
                />
                <text
                  textAnchor="middle"
                  y="4"
                  fill="var(--color-fg)"
                  fontSize={n.short.length > 4 ? 7 : 8}
                  fontFamily="IBM Plex Mono, ui-monospace, monospace"
                >
                  {n.short}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {(
          [
            ["runtime", "Runtime"],
            ["authoring", "Authoring"],
            ["grounding", "Grounding"],
            ["boundary", "Boundary"],
          ] as const
        ).map(([k, label]) => (
          <span key={k} className="inline-flex items-center gap-1.5 font-mono text-xs text-faint">
            <span
              className="inline-block h-px w-4"
              style={{
                background: EDGE_STROKE[k],
                borderTop: k === "authoring" || k === "boundary" ? "1px dashed currentColor" : undefined,
              }}
            />
            {label}
          </span>
        ))}
      </div>

      {open ? (
        <div
          className="fixed inset-0 z-40 bg-bg/50"
          onClick={() => onOpen(null)}
          aria-hidden
        />
      ) : null}

      <aside
        className={`fixed inset-x-0 bottom-0 z-50 mx-auto max-w-lg rounded-t-2xl bg-surface-2 p-5 ring-1 ring-border transition-transform duration-200 ${
          open ? "translate-y-0 pointer-events-auto" : "pointer-events-none translate-y-full"
        }`}
        aria-hidden={!open}
      >
        {open ? (
          <>
            <div className="mb-3 flex items-start justify-between gap-3">
              <div>
                <p className="font-mono text-xs uppercase tracking-wider text-faint">{open.ring}</p>
                <h3 className="text-lg font-semibold text-fg">{open.label}</h3>
              </div>
              <button
                type="button"
                onClick={() => onOpen(null)}
                className="flex h-11 w-11 items-center justify-center rounded-lg bg-surface ring-1 ring-border"
                aria-label="Close"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <span className={`inline-flex rounded-full px-2.5 py-1 font-mono text-xs ring-1 ${BADGE_CLASS[open.badge]}`}>
              {open.badge}
            </span>
            <p className="mt-3 text-sm leading-relaxed text-muted">{open.note}</p>
            {open.source ? (
              <p className="mt-2 font-mono text-xs text-faint">{open.source}</p>
            ) : null}
          </>
        ) : null}
      </aside>
    </div>
  );
}

function DoorsPanel() {
  return (
    <ol className="space-y-2">
      {DOORS.map((d, i) => (
        <li key={d.id} className="flex gap-3 rounded-xl bg-surface px-3 py-3 ring-1 ring-border">
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-surface-2 font-mono text-xs font-semibold text-accent-soft ring-1 ring-border">
            {i + 1}
          </span>
          <div>
            <p className="font-medium text-fg">{d.label}</p>
            <p className="text-sm text-muted">{d.detail}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

function FlowPanel() {
  return (
    <ol className="space-y-2">
      {FLOW.map((s, i) => (
        <li
          key={s.id}
          className={`rounded-xl bg-surface px-4 py-3 ring-1 ${
            s.kind === "real" ? "ring-info/35" : "ring-accent/25 border-dashed"
          }`}
        >
          <p className="font-mono text-xs uppercase tracking-wider text-faint">
            {i + 1} · {s.kind}
          </p>
          <p className="font-medium text-fg">{s.label}</p>
          <p className="text-sm text-muted">{s.detail}</p>
        </li>
      ))}
    </ol>
  );
}

function OwnershipPanel() {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <div className="rounded-xl bg-ok-bg p-4 ring-1 ring-ok/30">
        <p className="font-mono text-xs uppercase tracking-wider text-ok">Ours</p>
        <ul className="mt-2 space-y-2 text-sm text-fg">
          {OWNERSHIP.ours.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="rounded-xl bg-surface p-4 ring-1 ring-border">
        <p className="font-mono text-xs uppercase tracking-wider text-faint">Not claimed</p>
        <ul className="mt-2 space-y-2 text-sm text-muted">
          {OWNERSHIP.notOurs.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
