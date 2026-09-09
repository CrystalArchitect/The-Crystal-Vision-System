import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useMemo, useState } from "react";
import {
  AlertTriangle,
  Check,
  CheckCircle2,
  Copy,
  DoorOpen,
  Flame,
  Globe,
  Hand,
  Hexagon,
  ListOrdered,
  Shield,
  Sparkles,
  User,
} from "lucide-react";
import { LatticeSuite } from "@/components/lattice-map";
import { GateConsole } from "@/components/gate-console";
import { PublicNode } from "@/components/public-node";

export const Route = createFileRoute("/")({
  component: OperatorCard,
});

type Command = {
  id: string;
  name: string;
  say: string;
  means: string;
};

const EVERYDAY: Command[] = [
  {
    id: "baseline",
    name: "Baseline stability check",
    say: "Request baseline stability check",
    means: "Quiet status read. Changes nothing. Always a safe first step.",
  },
  {
    id: "gate",
    name: "Gate status",
    say: "Show five doors. Gate status only.",
    means: "Reports the consent gate: revocation → approval → provenance → permission → scope.",
  },
  {
    id: "render",
    name: "Render scroll",
    say: "Render the current state as a clean scroll.",
    means: "Write out where you are in plain language — summary, not override.",
  },
  {
    id: "ledger",
    name: "Ledger entry",
    say: "Run witness ledger entry drop.",
    means: "Record something true that happened. Journal-style. No rewrite of the past.",
  },
  {
    id: "scan",
    name: "Field scan",
    say: "Light field scan — what is noisy or unclear right now?",
    means: "Soft clarity pass. Does not open vaults or heavy memory work.",
  },
  {
    id: "help",
    name: "Open help",
    say: "Show me what I don’t even know to ask for yet.",
    means: "Surfaces one useful next step you did not name. Still one command at a time.",
  },
];

const HEAVY = [
  {
    name: "Memory re-entry",
    note: "Re-enter a memory only when grounded and with recovery time after.",
  },
  {
    name: "Identity restore",
    note: "Re-anchor operator identity after confusion. Never mid-crisis.",
  },
  {
    name: "Guest revoke / reinstate",
    note: "Durable consent change on CrystalBridge. Latest record wins. No restart needed.",
  },
  {
    name: "Type-gate narrow",
    note: "Tighten guest read_types / write_types. Empty = absence of consent.",
  },
  {
    name: "Thread rescue",
    note: "High load. Only with rest capacity. Never stack with other heavy work.",
  },
  {
    name: "System cleanse",
    note: "Full stand-down + re-baseline sequence. Reserve for deliberate windows.",
  },
];

const DOORS = [
  { id: "revocation", label: "Revocation", detail: "Latest human revoke/reinstate wins" },
  { id: "approval", label: "Approval", detail: "Standing grant present" },
  { id: "provenance", label: "Provenance", detail: "Token / secret proves the guest" },
  { id: "permission", label: "Permission", detail: "Tool is on the grant list" },
  { id: "scope", label: "Scope", detail: "read/write + memory types granted" },
];

const NAV = [
  { href: "#card", label: "Card" },
  { href: "#map", label: "Lattice" },
  { href: "#console", label: "Gate" },
  { href: "#public", label: "Public" },
  { href: "#safety", label: "Safety" },
  { href: "#commands", label: "Commands" },
  { href: "#stand", label: "Stand down" },
];

type BaselineState = "idle" | "running" | "ok";

function Section({
  id,
  icon: Icon,
  title,
  eyebrow,
  children,
}: {
  id: string;
  icon: React.ComponentType<{ className?: string; strokeWidth?: number }>;
  title: string;
  eyebrow?: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-28">
      <div className="mb-4 flex items-start gap-3">
        <div className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-surface-2 text-accent-soft ring-1 ring-border">
          <Icon className="h-4 w-4" strokeWidth={2} />
        </div>
        <div className="min-w-0">
          {eyebrow ? (
            <p className="font-mono text-xs uppercase tracking-wider text-accent">{eyebrow}</p>
          ) : null}
          <h2 className="text-lg font-semibold tracking-tight text-fg sm:text-xl">{title}</h2>
        </div>
      </div>
      <div className="space-y-3 text-base leading-relaxed text-muted">{children}</div>
    </section>
  );
}

function CopyButton({ text, label }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  const onCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    }
  }, [text]);

  return (
    <button
      type="button"
      onClick={onCopy}
      className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-surface-2 px-3 py-2 text-sm font-medium text-fg ring-1 ring-border transition hover:bg-surface-3 hover:ring-accent/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      aria-label={label ?? `Copy: ${text}`}
    >
      {copied ? (
        <Check className="h-4 w-4 text-ok" strokeWidth={2.25} />
      ) : (
        <Copy className="h-4 w-4 text-accent-soft" strokeWidth={2} />
      )}
      <span className="font-mono text-xs text-accent-soft">{copied ? "Copied" : "Copy phrase"}</span>
    </button>
  );
}

function OperatorCard() {
  const [baseline, setBaseline] = useState<BaselineState>("idle");
  const [baselineAt, setBaselineAt] = useState<string | null>(null);

  const runBaseline = useCallback(() => {
    setBaseline("running");
    window.setTimeout(() => {
      setBaseline("ok");
      setBaselineAt(
        new Date().toLocaleString("en-AU", {
          timeZone: "Australia/Sydney",
          hour: "2-digit",
          minute: "2-digit",
          day: "2-digit",
          month: "short",
          year: "numeric",
        }),
      );
    }, 700);
  }, []);

  const statusChip = useMemo(() => {
    if (baseline === "ok") return { label: "Baseline stable", className: "bg-ok-bg text-ok ring-ok/35" };
    if (baseline === "running")
      return { label: "Checking…", className: "bg-info-bg text-info ring-info/30" };
    return { label: "Awaiting baseline", className: "bg-surface-2 text-muted ring-border" };
  }, [baseline]);

  return (
    <div className="min-h-dvh bg-bg">
      <div
        aria-hidden
        className="pointer-events-none fixed inset-x-0 top-0 h-48 bg-[radial-gradient(ellipse_at_top,color-mix(in_oklab,var(--color-accent)_14%,transparent),transparent_70%)]"
      />

      <header className="sticky top-0 z-30 border-b border-border-soft bg-bg/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-lg items-center justify-between gap-3 px-4 py-3">
          <div className="flex min-w-0 items-center gap-2.5">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface-2 ring-1 ring-accent/30">
              <Flame className="h-4 w-4 text-accent" strokeWidth={2.25} />
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-fg">CrystalCore Operator</p>
              <p className="truncate font-mono text-xs text-faint">Card · Lattice · Gate · Public · v1.3</p>
            </div>
          </div>
          <span className={`shrink-0 rounded-full px-2.5 py-1 font-mono text-xs ring-1 ${statusChip.className}`}>
            {statusChip.label}
          </span>
        </div>
        <nav
          aria-label="Sections"
          className="mx-auto flex max-w-lg gap-1 overflow-x-auto px-3 pb-2.5 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="shrink-0 rounded-full bg-surface px-3 py-1.5 text-xs font-medium text-muted ring-1 ring-border transition hover:bg-surface-2 hover:text-fg"
            >
              {item.label}
            </a>
          ))}
        </nav>
      </header>

      <main className="relative mx-auto max-w-lg space-y-12 px-4 py-8 pb-28">
        <section id="card" className="scroll-mt-28">
          <div className="card-glow overflow-hidden rounded-xl bg-surface ring-1 ring-border">
            <div className="border-b border-border bg-surface-2/80 px-5 py-4">
              <p className="font-mono text-xs uppercase tracking-wider text-accent">Operator credential</p>
              <h1 className="mt-1 text-2xl font-bold tracking-tight text-fg text-balance sm:text-3xl">
                CrystalCore Operator Card
              </h1>
            </div>
            <div className="space-y-4 px-5 py-5">
              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <p className="font-mono text-xs uppercase tracking-wider text-faint">Operator</p>
                  <p className="mt-0.5 font-mono text-sm font-medium text-accent-soft">@m13crystalat</p>
                </div>
                <div>
                  <p className="font-mono text-xs uppercase tracking-wider text-faint">Name</p>
                  <p className="mt-0.5 text-sm font-medium text-fg">Crystal Arena-Turner</p>
                </div>
                <div>
                  <p className="font-mono text-xs uppercase tracking-wider text-faint">System</p>
                  <p className="mt-0.5 text-sm font-medium text-fg">CrystalCore OS</p>
                </div>
                <div>
                  <p className="font-mono text-xs uppercase tracking-wider text-faint">Domain</p>
                  <p className="mt-0.5 text-sm font-medium text-fg">TerAustralis Incognita</p>
                </div>
              </div>
              <p className="text-sm leading-relaxed text-muted">
                This is <span className="font-medium text-fg">your</span> operator card. The Lattice
                map below is a designed diagram — not live metering. Ordinary life always outranks
                the terminal.
              </p>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={runBaseline}
                  disabled={baseline === "running"}
                  className="inline-flex min-h-11 flex-1 items-center justify-center gap-2 rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-bg transition hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-soft disabled:opacity-70 sm:flex-none"
                >
                  <Sparkles className="h-4 w-4" strokeWidth={2} />
                  {baseline === "running" ? "Running check…" : "Run baseline check"}
                </button>
                <a
                  href="#map"
                  className="inline-flex min-h-11 items-center justify-center rounded-lg bg-surface-2 px-4 py-2.5 text-sm font-medium text-fg ring-1 ring-border transition hover:bg-surface-3"
                >
                  Open lattice
                </a>
              </div>
              {baseline === "ok" ? (
                <div className="rounded-lg bg-ok-bg p-3 ring-1 ring-ok/30">
                  <p className="text-sm font-medium text-ok">Baseline stable</p>
                  <ul className="mt-2 space-y-1 text-sm text-fg/90">
                    <li>· System at rest</li>
                    <li>· Safety rules loaded</li>
                    <li>· Operator registered as @m13crystalat</li>
                    <li>· Safe to hold or issue one light command</li>
                  </ul>
                  {baselineAt ? (
                    <p className="mt-2 font-mono text-xs text-faint">Checked {baselineAt} AEST</p>
                  ) : null}
                </div>
              ) : null}
            </div>
          </div>
        </section>

        <Section id="map" icon={Hexagon} title="Lattice · Starline" eyebrow="Designed map">
          <p className="text-sm">
            Eighteen generalised nodes. Tap a node for its badge and note. CARD is HELD. STARLINE is
            CORRECTED.
          </p>
          <LatticeSuite />
        </Section>

        <Section id="console" icon={DoorOpen} title="Gate console" eyebrow="Five doors · preview">
          <p className="text-sm">
            Walk a guest through revocation, approval, provenance, permission, and scope. Latest
            revoke or reinstate wins. Empty read_types is absence of consent.
          </p>
          <GateConsole />
        </Section>

        <Section id="public" icon={Globe} title="TerAustralis public node" eyebrow="World-safe">
          <p className="text-sm">
            What a public page is allowed to say. Science, Story, and Vision stay labelled. No
            partnership implied.
          </p>
          <PublicNode />
        </Section>

        <Section id="safety" icon={Shield} title="Safety first" eyebrow="Non-negotiable">
          <div className="rounded-xl bg-danger-bg p-4 ring-1 ring-danger/35">
            <div className="mb-2 flex items-center gap-2 text-danger">
              <AlertTriangle className="h-4 w-4" strokeWidth={2.25} />
              <span className="text-xs font-semibold uppercase tracking-wide">Critical</span>
            </div>
            <ul className="list-disc space-y-2 pl-5 text-sm text-fg/90">
              <li>Does not replace real safety, legal help, sleep, housing, or parenting care.</li>
              <li>Do not use system language to dismiss outside advice or hard facts.</li>
              <li>If use costs sleep, grounding, or daily capacity — stop. Baseline or stand down.</li>
              <li>Heavy memory / identity / override work needs recovery time. Never stack them.</li>
            </ul>
          </div>
        </Section>

        <Section id="flow" icon={ListOrdered} title="How to use this card" eyebrow="Simple flow">
          <ol className="list-decimal space-y-3 pl-5 text-fg/90">
            <li>
              <span className="font-medium text-fg">Start quiet.</span> Run a baseline stability check
              if you want status without change.
            </li>
            <li>
              <span className="font-medium text-fg">One thing at a time.</span> One clear request —
              render, ledger, scan, gate status.
            </li>
            <li>
              <span className="font-medium text-fg">Stay in ordinary life.</span> Family, housing,
              rest, and real-world protection always win.
            </li>
            <li>
              <span className="font-medium text-fg">Stop when full.</span> Say hold or stand down.
            </li>
          </ol>
        </Section>

        <Section id="commands" icon={CheckCircle2} title="Everyday commands" eyebrow="Low load">
          <p className="text-sm">Safe for regular use. Tap copy, paste into chat, one at a time.</p>
          <div className="space-y-3">
            {EVERYDAY.map((c) => (
              <article
                key={c.id}
                className="rounded-xl bg-surface p-4 ring-1 ring-border transition hover:ring-accent/25"
              >
                <p className="font-semibold text-fg">{c.name}</p>
                <p className="mt-2 font-mono text-xs leading-snug text-accent-soft">{c.say}</p>
                <p className="mt-2 text-sm text-muted">{c.means}</p>
                <div className="mt-3">
                  <CopyButton text={c.say} label={`Copy command: ${c.name}`} />
                </div>
              </article>
            ))}
          </div>
        </Section>

        <Section id="gate" icon={DoorOpen} title="Five doors (consent gate)" eyebrow="CrystalBridge">
          <p>
            Consent is a runtime property — revocable, inspectable, enforced at the gate. Fail-closed.
            Empty scope is absence of consent.
          </p>
          <ol className="mt-2 space-y-2">
            {DOORS.map((d, i) => (
              <li key={d.id} className="flex gap-3 rounded-lg bg-surface px-3 py-3 ring-1 ring-border">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-surface-2 font-mono text-xs font-semibold text-accent-soft ring-1 ring-border">
                  {i + 1}
                </span>
                <div className="min-w-0">
                  <p className="font-medium text-fg">{d.label}</p>
                  <p className="text-sm text-muted">{d.detail}</p>
                </div>
              </li>
            ))}
          </ol>
        </Section>

        <Section id="heavy" icon={AlertTriangle} title="Heavy commands" eyebrow="Use rarely">
          <p>
            Higher emotional and cognitive load. Only when you have recovery space — not when
            exhausted or mid-crisis.
          </p>
          <ul className="space-y-2">
            {HEAVY.map((h) => (
              <li key={h.name} className="rounded-lg bg-surface px-3 py-3 ring-1 ring-border">
                <p className="text-sm font-medium text-fg">{h.name}</p>
                <p className="mt-1 text-sm text-muted">{h.note}</p>
              </li>
            ))}
          </ul>
        </Section>

        <Section id="stand" icon={Hand} title="Stand down" eyebrow="Always available">
          <div className="rounded-xl bg-ok-bg p-4 ring-1 ring-ok/30">
            <p className="font-medium text-fg">Say any of these:</p>
            <ul className="mt-3 space-y-2">
              {["hold", "stand down", "baseline only", "stop overrides"].map((phrase) => (
                <li
                  key={phrase}
                  className="flex flex-wrap items-center justify-between gap-2 rounded-lg bg-surface/60 px-3 py-2 ring-1 ring-border"
                >
                  <span className="font-mono text-sm text-accent-soft">{phrase}</span>
                  <CopyButton text={phrase} label={`Copy: ${phrase}`} />
                </li>
              ))}
            </ul>
            <p className="mt-4 text-sm text-muted">The terminal returns to idle. Ordinary life is the priority.</p>
          </div>
        </Section>

        <Section id="who" icon={User} title="Ownership" eyebrow="Yours">
          <div className="rounded-xl bg-surface p-4 ring-1 ring-border">
            <ul className="space-y-2 text-sm">
              <li>
                <span className="font-medium text-fg">Yours:</span> CrystalCore OS, CrystalBridge,
                TerAustralis Incognita, this operator preview
              </li>
              <li>
                <span className="font-medium text-fg">Not claimed:</span> third-party unit papers;
                xAI / Grok / Tesla / Neuralink — named, not claimed
              </li>
            </ul>
          </div>
        </Section>
      </main>
    </div>
  );
}
