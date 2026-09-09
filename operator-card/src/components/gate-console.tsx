import { useMemo, useState } from "react";

const MEMORY_TYPES = ["episodic", "semantic", "reflective"] as const;
type MemType = (typeof MEMORY_TYPES)[number];

type GuestId = "guest-a" | "guest-b" | "guest-c";

type LedgerEntry = {
  id: string;
  at: string;
  guest: GuestId;
  action: "revoke" | "reinstate" | "ask" | "grant";
  detail: string;
};

type Grant = {
  approved: boolean;
  provenance: boolean;
  tools: string[];
  readTypes: MemType[];
};

const GUESTS: { id: GuestId; label: string; note: string }[] = [
  { id: "guest-a", label: "Full guest", note: "Standing grant. Read three types. Write semantic." },
  { id: "guest-b", label: "Restricted guest", note: "Standing grant. Semantic read only." },
  { id: "guest-c", label: "Unknown guest", note: "No standing grant. Fail-closed." },
];

const DEFAULT_GRANTS: Record<GuestId, Grant> = {
  "guest-a": {
    approved: true,
    provenance: true,
    tools: ["memory.read", "memory.write"],
    readTypes: ["episodic", "semantic", "reflective"],
  },
  "guest-b": {
    approved: true,
    provenance: true,
    tools: ["memory.read"],
    readTypes: ["semantic"],
  },
  "guest-c": {
    approved: false,
    provenance: false,
    tools: [],
    readTypes: [],
  },
};

function nowStamp() {
  return new Date().toLocaleString("en-AU", {
    timeZone: "Australia/Sydney",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

type DoorResult = { id: string; label: string; pass: boolean; why: string };

function evaluate(
  guest: GuestId,
  grant: Grant,
  revoked: boolean,
  tool: string,
  askTypes: MemType[],
): DoorResult[] {
  const doors: DoorResult[] = [];

  doors.push({
    id: "revocation",
    label: "1 · Revocation",
    pass: !revoked,
    why: revoked ? "Latest ledger line is revoke. Access refused." : "No active revoke.",
  });

  doors.push({
    id: "approval",
    label: "2 · Approval",
    pass: grant.approved,
    why: grant.approved ? "Standing grant present." : "No standing grant. Fail-closed.",
  });

  doors.push({
    id: "provenance",
    label: "3 · Provenance",
    pass: grant.provenance,
    why: grant.provenance ? "Guest token recognised." : "Guest not proven.",
  });

  doors.push({
    id: "permission",
    label: "4 · Permission",
    pass: grant.tools.includes(tool),
    why: grant.tools.includes(tool) ? `${tool} is on the grant list.` : `${tool} is not granted.`,
  });

  const missing = askTypes.filter((t) => !grant.readTypes.includes(t));
  const scopeOk = grant.readTypes.length > 0 && missing.length === 0;
  doors.push({
    id: "scope",
    label: "5 · Scope",
    pass: scopeOk,
    why:
      grant.readTypes.length === 0
        ? "Empty read_types is absence of consent."
        : missing.length
          ? `Refused types: ${missing.join(", ")}.`
          : `Allowed: ${grant.readTypes.join(", ")}. Conversation never guest-readable.`,
  });

  return doors;
}

export function GateConsole() {
  const [guest, setGuest] = useState<GuestId>("guest-a");
  const [revoked, setRevoked] = useState<Record<GuestId, boolean>>({
    "guest-a": false,
    "guest-b": false,
    "guest-c": false,
  });
  const [grants, setGrants] = useState(DEFAULT_GRANTS);
  const [tool, setTool] = useState("memory.read");
  const [askTypes, setAskTypes] = useState<MemType[]>(["semantic"]);
  const [ledger, setLedger] = useState<LedgerEntry[]>([]);
  const [lastCheck, setLastCheck] = useState<DoorResult[] | null>(null);

  const doors = useMemo(
    () => evaluate(guest, grants[guest], revoked[guest], tool, askTypes),
    [guest, grants, revoked, tool, askTypes],
  );
  const allowed = doors.every((d) => d.pass);

  function push(action: LedgerEntry["action"], detail: string, who: GuestId = guest) {
    setLedger((prev) =>
      [
        {
          id: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
          at: nowStamp(),
          guest: who,
          action,
          detail,
        },
        ...prev,
      ].slice(0, 12),
    );
  }

  function runCheck() {
    push("ask", `check ${tool} · types ${askTypes.join(",") || "(none)"}`);
    setLastCheck(doors);
  }

  function revoke() {
    setRevoked((r) => ({ ...r, [guest]: true }));
    push("revoke", "Latest record wins. No restart.");
    setLastCheck(null);
  }

  function reinstate() {
    setRevoked((r) => ({ ...r, [guest]: false }));
    push("reinstate", "Access restored. Latest record wins.");
    setLastCheck(null);
  }

  function toggleType(t: MemType) {
    setGrants((g) => {
      const cur = g[guest].readTypes;
      const next = cur.includes(t) ? cur.filter((x) => x !== t) : [...cur, t];
      return { ...g, [guest]: { ...g[guest], readTypes: next } };
    });
    push("grant", `read_types toggled: ${t}`);
    setLastCheck(null);
  }

  function toggleAsk(t: MemType) {
    setAskTypes((cur) => (cur.includes(t) ? cur.filter((x) => x !== t) : [...cur, t]));
  }

  return (
    <div className="space-y-4">
      <div className="rounded-xl bg-dust/25 px-4 py-3 ring-1 ring-dust">
        <p className="font-mono text-xs uppercase tracking-wider text-accent">Preview only</p>
        <p className="mt-1 text-sm text-muted">
          Local five-door simulator. Not connected to CrystalCore runtime. Consent is revocable,
          inspectable, fail-closed. Working conversation is never guest-readable.
        </p>
      </div>

      <div className="grid gap-2">
        {GUESTS.map((g) => (
          <button
            key={g.id}
            type="button"
            onClick={() => {
              setGuest(g.id);
              setLastCheck(null);
            }}
            className={`min-h-11 rounded-xl px-4 py-3 text-left ring-1 transition ${
              guest === g.id
                ? "bg-surface-3 ring-accent/50"
                : "bg-surface ring-border hover:bg-surface-2"
            }`}
          >
            <p className="text-sm font-medium text-fg">{g.label}</p>
            <p className="text-xs text-muted">{g.note}</p>
          </button>
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={revoke}
          className="min-h-11 rounded-lg bg-danger-bg px-4 text-sm font-medium text-danger ring-1 ring-danger/35"
        >
          Revoke
        </button>
        <button
          type="button"
          onClick={reinstate}
          className="min-h-11 rounded-lg bg-ok-bg px-4 text-sm font-medium text-ok ring-1 ring-ok/35"
        >
          Reinstate
        </button>
        <button
          type="button"
          onClick={runCheck}
          className="min-h-11 flex-1 rounded-lg bg-accent px-4 text-sm font-semibold text-bg sm:flex-none"
        >
          Run gate check
        </button>
      </div>

      <div>
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-faint">Ask tool</p>
        <div className="flex gap-2">
          {["memory.read", "memory.write"].map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setTool(t)}
              className={`min-h-11 rounded-lg px-3 font-mono text-xs ring-1 ${
                tool === t ? "bg-surface-3 text-fg ring-accent/40" : "bg-surface text-muted ring-border"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div>
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-faint">Ask types</p>
        <div className="flex flex-wrap gap-2">
          {MEMORY_TYPES.map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => toggleAsk(t)}
              className={`min-h-11 rounded-lg px-3 font-mono text-xs ring-1 ${
                askTypes.includes(t)
                  ? "bg-info-bg text-info ring-info/30"
                  : "bg-surface text-muted ring-border"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div>
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-faint">
          Grant read_types (this guest)
        </p>
        <div className="flex flex-wrap gap-2">
          {MEMORY_TYPES.map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => toggleType(t)}
              className={`min-h-11 rounded-lg px-3 font-mono text-xs ring-1 ${
                grants[guest].readTypes.includes(t)
                  ? "bg-ok-bg text-ok ring-ok/35"
                  : "bg-surface text-muted ring-border"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        {(lastCheck ?? doors).map((d) => (
          <div
            key={d.id}
            className={`flex gap-3 rounded-xl px-3 py-3 ring-1 ${
              d.pass ? "bg-ok-bg ring-ok/25" : "bg-danger-bg ring-danger/25"
            }`}
          >
            <span
              className={`mt-0.5 h-2.5 w-2.5 shrink-0 rounded-full ${d.pass ? "bg-ok" : "bg-danger"}`}
            />
            <div>
              <p className="text-sm font-medium text-fg">{d.label}</p>
              <p className="text-sm text-muted">{d.why}</p>
            </div>
          </div>
        ))}
      </div>

      <p
        className={`rounded-xl px-4 py-3 text-sm font-medium ring-1 ${
          allowed ? "bg-ok-bg text-ok ring-ok/30" : "bg-danger-bg text-danger ring-danger/30"
        }`}
      >
        {allowed ? "Pass — guest may proceed under this scope." : "Refuse — fail-closed at first failed door."}
      </p>

      <div>
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-faint">
          Observable ask / revoke ledger
        </p>
        {ledger.length === 0 ? (
          <p className="text-sm text-muted">Empty. Asks are logged before the reply.</p>
        ) : (
          <ul className="space-y-1.5">
            {ledger.map((row) => (
              <li key={row.id} className="rounded-lg bg-surface px-3 py-2 font-mono text-xs text-muted ring-1 ring-border">
                <span className="text-faint">{row.at}</span> · {row.guest} · {row.action} · {row.detail}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
