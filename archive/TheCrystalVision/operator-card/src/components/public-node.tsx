const LAYERS = [
  {
    id: "science",
    label: "Science",
    body: "What is measured or merged: five-door consent, type-gates, observable ask, music catalogue, Lattice map on the public site.",
  },
  {
    id: "story",
    label: "Story",
    body: "Red dust, starlines. Story as Bridge — not doctrine, not a claim of Country.",
  },
  {
    id: "vision",
    label: "Vision",
    body: "Australia as a multiplanetary logistics and ethics node. Proposal, not a contract. Named companies are not partners.",
  },
] as const;

const STATUS = [
  { badge: "LIVE", item: "Lattice · Starline map (public site)" },
  { badge: "MERGED", item: "Five-door consent + observable ask" },
  { badge: "MERGED", item: "Section VI motion plates V02–V04 (unpublished by allowlist)" },
  { badge: "MERGED", item: "Music catalogue + rebuilt manifest" },
  { badge: "HELD", item: "This operator preview (not a repo surface)" },
  { badge: "PARKED", item: "SAT dedicated-repo split — needs add_repo grant" },
  { badge: "PARKED", item: "ots stamp mythos/MANIFEST.sha256" },
] as const;

const BADGE: Record<string, string> = {
  LIVE: "bg-ok-bg text-ok ring-ok/35",
  MERGED: "bg-info-bg text-info ring-info/30",
  HELD: "bg-surface-3 text-muted ring-border",
  PARKED: "bg-dust/30 text-accent-soft ring-dust",
};

export function PublicNode() {
  return (
    <div className="space-y-4">
      <div className="rounded-xl bg-dust/25 px-4 py-3 ring-1 ring-dust">
        <p className="font-mono text-xs uppercase tracking-wider text-accent">World-safe node</p>
        <p className="mt-1 text-sm text-muted">
          Designed public face. Personal handles stay off this layer. Homage, not ownership. Named,
          not claimed.
        </p>
      </div>

      <article className="card-glow overflow-hidden rounded-xl bg-surface ring-1 ring-border">
        <div className="border-b border-border bg-surface-2/80 px-5 py-4">
          <p className="font-mono text-xs uppercase tracking-wider text-accent">TerAustralis Incognita™</p>
          <h3 className="mt-1 text-xl font-semibold tracking-tight text-fg">Public node</h3>
        </div>
        <div className="space-y-3 px-5 py-4 text-sm leading-relaxed text-muted">
          <p>
            An Australian-built vision for a multiplanetary logistics and consent culture — red earth
            to starline. This node states what is authored here. It does not imply access, funding, or
            partnership with any named company.
          </p>
          <p className="font-mono text-xs text-faint">ABN 70 741 068 059 · All rights reserved</p>
        </div>
      </article>

      <div className="grid gap-3">
        {LAYERS.map((layer) => (
          <div key={layer.id} className="rounded-xl bg-surface px-4 py-3 ring-1 ring-border">
            <p className="font-mono text-xs uppercase tracking-wider text-accent">{layer.label}</p>
            <p className="mt-1 text-sm text-muted">{layer.body}</p>
          </div>
        ))}
      </div>

      <div>
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-faint">Status ledger</p>
        <ul className="space-y-2">
          {STATUS.map((row) => (
            <li
              key={row.item}
              className="flex items-start gap-3 rounded-xl bg-surface px-3 py-3 ring-1 ring-border"
            >
              <span
                className={`mt-0.5 shrink-0 rounded-full px-2 py-0.5 font-mono text-xs ring-1 ${BADGE[row.badge]}`}
              >
                {row.badge}
              </span>
              <span className="text-sm text-fg">{row.item}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <div className="rounded-xl bg-ok-bg p-4 ring-1 ring-ok/30">
          <p className="font-mono text-xs uppercase tracking-wider text-ok">Authored here</p>
          <ul className="mt-2 space-y-1 text-sm text-fg">
            <li>CrystalCore OS</li>
            <li>CrystalBridge consent gate</li>
            <li>TerAustralis Incognita</li>
            <li>Synthetic Affect Theory (project name)</li>
          </ul>
        </div>
        <div className="rounded-xl bg-surface p-4 ring-1 ring-border">
          <p className="font-mono text-xs uppercase tracking-wider text-faint">Not claimed</p>
          <ul className="mt-2 space-y-1 text-sm text-muted">
            <li>xAI / Grok / Tesla / Neuralink</li>
            <li>Country and Songline knowledge</li>
            <li>Third-party unit papers</li>
            <li>Any implied corporate partnership</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
