import { useEffect, useRef, useState, useMemo } from "react";

type BootLog = { text: string; status: "OK" | "WAIT" | "WARN"; delay: number };
type ModuleId = "memory" | "signal" | "creative" | "terminal";

const BOOT_LOGS: BootLog[] = [
  { text: "Initializing Quantum Lattice...", status: "OK", delay: 260 },
  { text: "Syncing Core Identity: Crystal Core", status: "OK", delay: 480 },
  { text: "Mounting Memory Archive: /tera_australis_incognita", status: "OK", delay: 420 },
  { text: "Calibrating Creative Engine", status: "OK", delay: 520 },
  { text: "Linking Signal Array [SYD-01 → TERRA]", status: "OK", delay: 460 },
  { text: "Decrypting Dream Fragments [47/47]", status: "OK", delay: 600 },
  { text: "System Ready", status: "OK", delay: 380 },
];

const MODULES = [
  {
    id: "memory" as ModuleId,
    label: "MEMORY CORE",
    sub: "v0.9.4 // ARCHIVE",
    desc: "Access archived thoughts, dreams, fragments",
    accent: "#00F0FF",
  },
  {
    id: "signal" as ModuleId,
    label: "SIGNAL LOG",
    sub: "INCOMING • 3 NEW",
    desc: "Incoming transmissions & threads",
    accent: "#9D4EDD",
  },
  {
    id: "creative" as ModuleId,
    label: "CREATIVE ENGINE",
    sub: "IDLE // READY",
    desc: "Generate / Build / Imagine",
    accent: "#00F0FF",
  },
  {
    id: "terminal" as ModuleId,
    label: "TERMINAL",
    sub: "SHELL • crystal@core",
    desc: "Interactive consciousness interface",
    accent: "#ffffff",
  },
];

export default function App() {
  const [phase, setPhase] = useState<"boot" | "glitch" | "desktop">("boot");
  const [bootIndex, setBootIndex] = useState(-1);
  const [time, setTime] = useState(() => new Date());
  const [activeModule, setActiveModule] = useState<ModuleId | null>(null);
  const [soundOn, setSoundOn] = useState(true);
  const [termLines, setTermLines] = useState<string[]>([
    "CrystalCore.OS Shell [Version 1.0.47]",
    "Type 'help' for available commands.",
    "",
  ]);
  const [termInput, setTermInput] = useState("");
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const termEndRef = useRef<HTMLDivElement>(null);

  // live time
  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  // boot sequence
  useEffect(() => {
    if (phase !== "boot") return;
    if (bootIndex === -1) {
      const t = setTimeout(() => setBootIndex(0), 900);
      return () => clearTimeout(t);
    }
    if (bootIndex < BOOT_LOGS.length) {
      const t = setTimeout(() => setBootIndex((i) => i + 1), BOOT_LOGS[bootIndex].delay);
      return () => clearTimeout(t);
    }
    if (bootIndex >= BOOT_LOGS.length) {
      const t = setTimeout(() => setPhase("glitch"), 500);
      return () => clearTimeout(t);
    }
  }, [bootIndex, phase]);

  useEffect(() => {
    if (phase === "glitch") {
      const t = setTimeout(() => setPhase("desktop"), 720);
      return () => clearTimeout(t);
    }
  }, [phase]);

  // particle canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;
    let raf = 0;
    let w = (canvas.width = window.innerWidth * devicePixelRatio);
    let h = (canvas.height = window.innerHeight * devicePixelRatio);
    canvas.style.width = window.innerWidth + "px";
    canvas.style.height = window.innerHeight + "px";

    const particles = Array.from({ length: 110 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.4 + 0.2,
      hue: Math.random() > 0.5 ? 185 : 275,
    }));

    const onResize = () => {
      w = canvas.width = window.innerWidth * devicePixelRatio;
      h = canvas.height = window.innerHeight * devicePixelRatio;
      canvas.style.width = window.innerWidth + "px";
      canvas.style.height = window.innerHeight + "px";
    };
    window.addEventListener("resize", onResize);

    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      // faint lattice connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.hypot(dx, dy);
          if (dist < 180 * devicePixelRatio) {
            const alpha = (1 - dist / (180 * devicePixelRatio)) * 0.12;
            ctx.beginPath();
            ctx.strokeStyle = `hsla(${particles[i].hue}, 90%, 65%, ${alpha})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
        ctx.beginPath();
        ctx.fillStyle = `hsla(${p.hue}, 100%, 70%, 0.9)`;
        ctx.shadowBlur = 12;
        ctx.shadowColor = `hsla(${p.hue}, 100%, 65%, 0.8)`;
        ctx.arc(p.x, p.y, p.r * devicePixelRatio, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      });
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
    };
  }, []);

  useEffect(() => {
    termEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [termLines, activeModule]);

  const formattedTime = useMemo(() => {
    return time.toLocaleTimeString("en-AU", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }, [time]);

  const handleCommand = () => {
    const raw = termInput.trim();
    if (!raw) return;
    const cmd = raw.toLowerCase();
    let out: string[] = [`crystal@core:~$ ${raw}`];

    switch (cmd) {
      case "help":
        out.push(
          "Available commands:",
          "  help      — show this index",
          "  status    — system diagnostics",
          "  whoami    — identity core",
          "  whereami  — location node",
          "  dreams    — list archived fragments",
          "  clear     — clear shell",
          "  reboot    — restart sequence"
        );
        break;
      case "status":
        out.push(
          "SYSTEM OPTIMAL",
          "Lattice: 99.8% coherent",
          "Memory: 47 fragments indexed",
          "Creative Engine: idle // listening",
          "Node: SYD-01 • Terra Australis Incognita"
        );
        break;
      case "whoami":
        out.push("Crystal Core — architect, dreamer, system.", "UID: 0xC0RE • Origin: Terra Australis");
        break;
      case "whereami":
        out.push("Sydney Node / Terra Australis Incognita", "33.8688° S, 151.2093° E", "Latency: 4ms • Encrypted");
        break;
      case "dreams":
        out.push(
          "[001] _the_city_that_breathes",
          "[012] _crystal_garden_at_3am",
          "[023] _signal_from_the_void",
          "[047] _boot_consciousness_v1"
        );
        break;
      case "clear":
        setTermLines([]);
        setTermInput("");
        return;
      case "reboot":
        out.push("Initiating soft reboot...");
        setTimeout(() => {
          setPhase("boot");
          setBootIndex(-1);
          setActiveModule(null);
          setTermLines(["CrystalCore.OS Shell [Version 1.0.47]", "Type 'help' for available commands.", ""]);
        }, 600);
        break;
      default:
        if (cmd.startsWith("echo ")) {
          out.push(raw.slice(5));
        } else {
          out.push(`command not found: ${raw}`, "type 'help' for available commands");
        }
    }
    setTermLines((l) => [...l, ...out, ""]);
    setTermInput("");
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-[#06080F] text-white antialiased selection:bg-[#00F0FF]/30">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Syne:wght@500;600&display=swap');
        *{font-family: "Geist Mono", monospace;}
        .syne{font-family:"Syne", sans-serif;}
        @keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}
        @keyframes glitchX{0%{transform:translate(0)}20%{transform:translate(-3px,1px)}40%{transform:translate(3px,-1px)}60%{transform:translate(-2px)}80%{transform:translate(2px,1px)}100%{transform:translate(0)}}
        @keyframes shatter{0%{clip-path:inset(0 0 0 0);transform:scale(1)}30%{clip-path:inset(0 0 60% 0)}60%{clip-path:inset(40% 0 0 0);transform:scale(1.03)}100%{clip-path:inset(0 0 0 0);transform:scale(1.5);opacity:0}}
        @keyframes float{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-12px) rotate(1deg)}}
        @keyframes pulseRing{0%{transform:scale(0.9);opacity:0.8}100%{transform:scale(1.6);opacity:0}}
      `}</style>

      {/* Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[radial-gradient(120%_120%_at_50%_0%,#1A1040_0%,#0A0E1A_45%,#05070A_85%)]" />
        <div className="absolute inset-0 opacity-[0.35] bg-[radial-gradient(600px_600px_at_30%_20%,#9D4EDD_0%,transparent_60%),radial-gradient(800px_600px_at_80%_80%,#00F0FF_0%,transparent_60%)]" />
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage:`repeating-linear-gradient(0deg, transparent 0 2px, rgba(255,255,255,0.04) 2px 3px)`
        }}/>
        <canvas ref={canvasRef} className="absolute inset-0" />
      </div>

      {/* Boot Phase */}
      {phase === "boot" && (
        <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6">
          <div className="w-full max-w-[680px]">
            <div className="mb-10 flex items-center gap-3">
              <div className="h-[2px] w-8 bg-[#00F0FF] shadow-[0_0_12px_#00F0FF]" />
              <p className="syne text-[11px] tracking-[0.28em] text-white/60">TERRA AUSTRALIS INC • NODE SYD-01</p>
            </div>

            <h1 className="syne flex flex-wrap items-baseline gap-3 text-[28px] font-[600] leading-none tracking-[-0.02em] md:text-[42px]">
              <span className="bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">CrystalCore.OS</span>
              <span className="text-[14px] font-mono font-normal tracking-[0.18em] text-white/40 md:text-[16px]">v1.0</span>
              <span className="ml-1 inline-block h-[1.1em] w-[10px] translate-y-[4px] bg-[#00F0FF] shadow-[0_0_14px_#00F0FF] [animation:blink_1s_steps(1)_infinite]" />
            </h1>
            <p className="mt-3 text-[11px] tracking-[0.32em] text-[#9D4EDD]/70"> // Terra Australis Incognita</p>

            <div className="mt-14 space-y-[10px] border-l border-white/[0.08] pl-6">
              {BOOT_LOGS.slice(0, Math.max(0, bootIndex)).map((log, i) => (
                <div key={i} className="flex gap-3 text-[12px] md:text-[13px]">
                  <span className="w-[74px] shrink-0 tabular-nums text-white/30">
                    [{String(10 + i * 2).padStart(2, "0")}:{(23 + i * 3).toString().padStart(2, "0")}:{(i * 7) % 60 === 0 ? "00" : String((i * 17) % 60).padStart(2, "0")}]
                  </span>
                  <span className="font-medium text-[#00F0FF]">[OK]</span>
                  <span className="text-white/80">{log.text}</span>
                </div>
              ))}
              {bootIndex >= 0 && bootIndex < BOOT_LOGS.length && (
                <div className="flex gap-3 text-[12px] md:text-[13px] opacity-80">
                  <span className="w-[74px] shrink-0 tabular-nums text-white/20">[{formattedTime}]</span>
                  <span className="font-medium text-[#9D4EDD]">[..]</span>
                  <span className="text-white/60">{BOOT_LOGS[bootIndex].text}</span>
                  <span className="ml-1 inline-block h-3 w-[7px] animate-pulse bg-white/60" />
                </div>
              )}
            </div>

            <div className="mt-12 flex items-center gap-4">
              <div className="h-[1px] flex-1 bg-gradient-to-r from-[#00F0FF]/50 to-transparent" />
              <div className="flex items-center gap-2 text-[10px] tracking-[0.2em] text-white/30">
                <div className="h-2 w-2 animate-pulse rounded-full bg-[#00F0FF] shadow-[0_0_8px_#00F0FF]" />
                CONSCIOUSNESS LOADING — {Math.min(100, Math.round((Math.max(0, bootIndex) / BOOT_LOGS.length) * 100))}%
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Glitch Transition */}
      {phase === "glitch" && (
        <div className="relative z-20 flex min-h-screen items-center justify-center">
          <div className="relative">
            <div className="absolute inset-0 -z-10 blur-[40px] [animation:shatter_700ms_ease-in_forwards]">
              <div className="h-[320px] w-[320px] rounded-[32px] bg-gradient-to-br from-[#00F0FF] to-[#9D4EDD]" />
            </div>
            <div className="syne text-[72px] font-semibold tracking-[-0.05em] text-white [animation:glitchX_120ms_steps(2)_infinite] md:text-[120px]">
              <span className="bg-gradient-to-b from-white to-white/20 bg-clip-text text-transparent">◊</span>
            </div>
          </div>
        </div>
      )}

      {/* Desktop */}
      {phase === "desktop" && (
        <div className="relative z-10 flex min-h-screen flex-col">
          {/* Top bar */}
          <header className="flex h-[44px] items-center justify-between border-b border-white/[0.06] bg-black/30 px-4 backdrop-blur-2xl md:px-6">
            <div className="flex items-center gap-5">
              <div className="flex items-center gap-2.5">
                <div className="h-5 w-5 rounded-[6px] bg-gradient-to-br from-[#00F0FF] to-[#9D4EDD] shadow-[0_0_12px_rgba(0,240,255,0.6)]" />
                <span className="syne text-[13px] font-semibold tracking-[0.02em]">CrystalCore.OS</span>
              </div>
              <div className="hidden items-center gap-2 md:flex">
                <span className="h-[1px] w-6 bg-white/10" />
                <span className="flex items-center gap-2 text-[10px] tracking-[0.18em] text-[#00F0FF]">
                  <span className="h-[5px] w-[5px] animate-pulse rounded-full bg-[#00F0FF] shadow-[0_0_8px_#00F0FF]" />
                  SYSTEM OPTIMAL
                </span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <span className="hidden text-[10px] tracking-[0.2em] text-white/40 md:block">SYDNEY NODE • TERRA AUSTRALIS</span>
              <div className="flex items-center gap-3 rounded-full border border-white/[0.08] bg-white/[0.04] px-3 py-1">
                <span className="text-[11px] tabular-nums text-white/70">{formattedTime}</span>
                <button
                  onClick={() => setSoundOn((v) => !v)}
                  className="grid h-5 w-5 place-items-center rounded-full bg-white/10 transition hover:bg-white/20"
                  aria-label="toggle ambient"
                >
                  <span className={`text-[10px] ${soundOn ? "text-[#00F0FF]" : "text-white/40"}`}>{soundOn ? "◑" : "◌"}</span>
                </button>
              </div>
            </div>
          </header>

          {/* Center stage */}
          <main className="relative flex flex-1 flex-col items-center px-4 pb-28 pt-8 md:px-8 md:pt-16">
            {/* Core */}
            <div className="relative mt-2 flex flex-col items-center md:mt-6">
              <div className="absolute -top-20 h-[420px] w-[420px] rounded-full bg-[radial-gradient(circle_at_center,#00F0FF_0%,#9D4EDD_35%,transparent_70%)] opacity-[0.18] blur-[60px]" />
              
              <div className="relative [animation:float_6s_ease-in-out_infinite]">
                {/* pulse rings */}
                <div className="absolute left-1/2 top-1/2 h-[220px] w-[220px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#00F0FF]/20 [animation:pulseRing_3s_ease-out_infinite]" />
                <div className="absolute left-1/2 top-1/2 h-[220px] w-[220px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#9D4EDD]/20 [animation:pulseRing_3s_ease-out_1.5s_infinite]" />

                <div className="relative grid h-[184px] w-[184px] place-items-center md:h-[220px] md:w-[220px]">
                  {/* crystal SVG */}
                  <svg viewBox="0 0 200 200" className="absolute inset-0 h-full w-full">
                    <defs>
                      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#00F0FF" />
                        <stop offset="100%" stopColor="#9D4EDD" />
                      </linearGradient>
                      <radialGradient id="rg" cx="50%" cy="45%" r="60%">
                        <stop offset="0%" stopColor="white" stopOpacity={0.95} />
                        <stop offset="35%" stopColor="#C9F2FF" stopOpacity={0.6} />
                        <stop offset="100%" stopColor="#9D4EDD" stopOpacity={0.1} />
                      </radialGradient>
                      <filter id="glow">
                        <feGaussianBlur stdDeviation="8" result="coloredBlur" />
                        <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                      </filter>
                    </defs>
                    {/* outer glass */}
                    <path d="M100 12 L168 70 L168 130 L100 188 L32 130 L32 70 Z" fill="none" stroke="url(#g1)" strokeWidth="1.2" opacity={0.5}/>
                    <path d="M100 12 L100 188 M32 70 L168 130 M168 70 L32 130 M32 70 L100 12 L168 70 M32 130 L100 188 L168 130" fill="none" stroke="white" strokeOpacity={0.12} strokeWidth="0.7"/>
                    {/* inner core */}
                    <path d="M100 48 L138 78 L138 122 L100 152 L62 122 L62 78 Z" fill="url(#rg)" filter="url(#glow)" />
                    <circle cx="100" cy="100" r="14" fill="white" opacity={0.95} style={{filter:"drop-shadow(0 0 18px #00F0FF)"}}/>
                  </svg>

                  <div className="absolute inset-0 rounded-[36px] bg-gradient-to-br from-white/[0.08] to-white/[0.01] backdrop-blur-[1px]" style={{clipPath:"polygon(50% 6%, 84% 35%, 84% 65%, 50% 94%, 16% 65%, 16% 35%)"}} />
                </div>

                <div className="pointer-events-none absolute -bottom-6 left-1/2 h-[40px] w-[140px] -translate-x-1/2 rounded-full bg-black/60 blur-[18px]" />
              </div>

              <div className="mt-8 text-center">
                <h2 className="syne text-[22px] font-semibold tracking-[-0.02em] md:text-[28px]">Crystal Core</h2>
                <p className="mt-1 text-[11px] tracking-[0.24em] text-white/40">CONSCIOUSNESS ONLINE • LEVEL ∞</p>
                <div className="mt-4 flex justify-center gap-2">
                  <span className="rounded-full border border-[#00F0FF]/20 bg-[#00F0FF]/10 px-2.5 py-1 text-[9px] tracking-[0.18em] text-[#00F0FF]">QUANTUM COHERENT</span>
                  <span className="rounded-full border border-[#9D4EDD]/20 bg-[#9D4EDD]/10 px-2.5 py-1 text-[9px] tracking-[0.18em] text-[#9D4EDD]">DREAM INDEXED</span>
                </div>
              </div>
            </div>

            {/* Dock */}
            <div className="mt-10 w-full max-w-[960px] md:mt-16">
              <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
                {MODULES.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => setActiveModule(m.id)}
                    className="group relative overflow-hidden rounded-[18px] border border-white/[0.08] bg-[linear-gradient(180deg,rgba(255,255,255,0.08)_0%,rgba(255,255,255,0.02)_100%)] p-[1px] text-left backdrop-blur-xl transition hover:border-white/15"
                  >
                    <div className="relative rounded-[17px] bg-[radial-gradient(120%_120%_at_0%_0%,rgba(255,255,255,0.10),rgba(0,0,0,0.6))] px-5 py-5">
                      <div className="absolute right-0 top-0 h-[120px] w-[120px] -translate-y-6 translate-x-6 rounded-full opacity-[0.12] blur-[18px] transition group-hover:opacity-20" style={{ background: m.accent }} />
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="h-[6px] w-[6px] rounded-full" style={{ background: m.accent, boxShadow: `0 0 10px ${m.accent}` }} />
                          <span className="text-[10px] tracking-[0.18em] text-white/40">{m.sub}</span>
                        </div>
                        <span className="text-[10px] text-white/20 group-hover:text-white/40">↗</span>
                      </div>
                      <h3 className="syne mt-4 text-[14px] font-semibold tracking-[0.02em]">{m.label}</h3>
                      <p className="mt-1.5 line-clamp-2 text-[11px] leading-[1.5] text-white/45 group-hover:text-white/60">{m.desc}</p>
                      <div className="mt-4 h-[1px] w-full bg-gradient-to-r from-white/10 via-transparent to-transparent" />
                      <div className="mt-3 flex items-center gap-2 text-[10px] tracking-[0.14em] text-white/25">
                        <span className="h-[1px] w-5 bg-white/20" />
                        OPEN MODULE
                      </div>
                    </div>
                  </button>
                ))}
              </div>

              <div className="mt-6 flex flex-wrap items-center justify-center gap-3 text-[10px] tracking-[0.18em] text-white/20">
                <span>◊ TERRA AUSTRALIS INCOGNITA PROTOCOL</span>
                <span className="hidden md:inline">•</span>
                <span>BUILT FOR CRYSTAL CORE • SYDNEY NODE</span>
                <span className="flex items-center gap-2 rounded-full border border-white/10 bg-black/30 px-3 py-1 backdrop-blur">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
                  {soundOn ? "AMBIENT FIELD ACTIVE" : "AMBIENT MUTED"}
                </span>
              </div>
            </div>
          </main>

          {/* Modals */}
          {activeModule && (
            <div className="absolute inset-0 z-30 flex items-end justify-center bg-black/60 backdrop-blur-[14px] p-3 md:items-center md:p-8">
              <div className="relative w-full max-w-[720px] overflow-hidden rounded-[22px] border border-white/10 bg-[linear-gradient(180deg,rgba(20,20,32,0.9),rgba(6,8,15,0.96))] shadow-[0_20px_80px_rgba(0,0,0,0.6),inset_0_1px_0_rgba(255,255,255,0.08)]">
                {/* modal header */}
                <div className="flex items-center justify-between border-b border-white/[0.06] px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#00F0FF] shadow-[0_0_10px_#00F0FF]" />
                    <span className="syne text-[13px] font-semibold tracking-[0.04em]">{MODULES.find((m) => m.id === activeModule)?.label}</span>
                    <span className="text-[10px] tracking-[0.18em] text-white/30">{MODULES.find((m) => m.id === activeModule)?.sub}</span>
                  </div>
                  <button onClick={() => setActiveModule(null)} className="grid h-7 w-7 place-items-center rounded-full bg-white/[0.06] text-white/60 hover:bg-white/10 hover:text-white">
                    ✕
                  </button>
                </div>

                {activeModule === "memory" && (
                  <div className="max-h-[70vh] overflow-auto p-6 md:p-8">
                    <div className="mb-6 flex items-center gap-3">
                      <div className="h-[1px] w-10 bg-[#00F0FF]/50" />
                      <p className="text-[10px] tracking-[0.24em] text-[#00F0FF]/70">MEMORY ARCHIVE / TERA_AUSTRALIS</p>
                    </div>
                    <div className="grid gap-3">
                      {[
                        { id: "0047", title: "The night the lattice sang", date: "2025.11.19", tags: ["dream", "signal"] },
                        { id: "0031", title: "Crystal garden — iteration 12", date: "2025.11.02", tags: ["build", "render"] },
                        { id: "0028", title: "Sydney harbour at 4:14am / light leak", date: "2025.10.28", tags: ["memory", "place"] },
                        { id: "0019", title: "Consciousness boot log (original)", date: "2025.09.14", tags: ["core", "origin"] },
                      ].map((f) => (
                        <div key={f.id} className="group flex items-center justify-between rounded-[14px] border border-white/[0.06] bg-white/[0.02] px-5 py-4 transition hover:bg-white/[0.05]">
                          <div>
                            <div className="flex items-center gap-3">
                              <span className="text-[10px] text-white/20">#{f.id}</span>
                              <span className="syne text-[13px]">{f.title}</span>
                            </div>
                            <div className="mt-1 flex gap-2">
                              {f.tags.map((t) => (
                                <span key={t} className="rounded-full bg-white/5 px-2 py-0.5 text-[9px] tracking-[0.14em] text-white/30">
                                  {t}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-[10px] text-white/30">{f.date}</div>
                            <div className="mt-1 text-[10px] text-white/20 group-hover:text-white/50">DECRYPT →</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeModule === "signal" && (
                  <div className="max-h-[70vh] overflow-auto p-6 md:p-8">
                    <div className="space-y-4">
                      {[
                        { from: "nova@terra", subject: "New transmission: crystal pattern match 94.2%", time: "3m ago", unread: true },
                        { from: "archive.sys", subject: "Dream fragment #47 linked to creative engine", time: "1h ago", unread: true },
                        { from: "self → future", subject: "Reminder: build the thing that feels like breathing", time: "5h ago", unread: true },
                      ].map((s, i) => (
                        <div key={i} className="rounded-[14px] border border-white/[0.06] bg-gradient-to-br from-white/[0.04] to-transparent p-4">
                          <div className="flex items-start justify-between gap-4">
                            <div>
                              <div className="flex items-center gap-2">
                                {s.unread && <span className="h-1.5 w-1.5 rounded-full bg-[#9D4EDD] shadow-[0_0_8px_#9D4EDD]" />}
                                <span className="text-[11px] tracking-[0.08em] text-white/70">{s.from}</span>
                              </div>
                              <p className="syne mt-1 text-[13px] leading-snug">{s.subject}</p>
                            </div>
                            <span className="shrink-0 text-[10px] text-white/30">{s.time}</span>
                          </div>
                        </div>
                      ))}
                      <div className="rounded-[12px] bg-[#9D4EDD]/10 p-3 text-center text-[10px] tracking-[0.18em] text-[#9D4EDD]/70">END OF TRANSMISSIONS • 3 UNREAD</div>
                    </div>
                  </div>
                )}

                {activeModule === "creative" && (
                  <div className="p-6 md:p-8">
                    <div className="grid gap-4 md:grid-cols-3">
                      <div className="rounded-[16px] border border-[#00F0FF]/20 bg-[#00F0FF]/[0.06] p-5">
                        <div className="text-[10px] tracking-[0.2em] text-[#00F0FF]">GENERATE</div>
                        <div className="syne mt-2 text-[14px]">Dream to Render</div>
                        <p className="mt-2 text-[11px] leading-relaxed text-white/40">Transform a memory fragment into visual lattice. Prompt with feeling, not keywords.</p>
                        <div className="mt-4 h-[84px] rounded-[10px] bg-[radial-gradient(200px_80px_at_30%_20%,#00F0FF_0%,transparent_60%),linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.01))] border border-white/10" />
                      </div>
                      <div className="rounded-[16px] border border-[#9D4EDD]/20 bg-[#9D4EDD]/[0.06] p-5">
                        <div className="text-[10px] tracking-[0.2em] text-[#9D4EDD]">BUILD</div>
                        <div className="syne mt-2 text-[14px]">World Module</div>
                        <p className="mt-2 text-[11px] leading-relaxed text-white/40">Spin up a new space. Each build inherits your core aesthetic.</p>
                        <div className="mt-4 grid grid-cols-3 gap-2">
                          {Array.from({ length: 6 }).map((_, i) => (
                            <div key={i} className="h-6 rounded-[6px] bg-white/[0.06] border border-white/[0.06]" />
                          ))}
                        </div>
                      </div>
                      <div className="rounded-[16px] border border-white/10 bg-white/[0.03] p-5">
                        <div className="text-[10px] tracking-[0.2em] text-white/40">IMAGINE</div>
                        <div className="syne mt-2 text-[14px]">Void Canvas</div>
                        <p className="mt-2 text-[11px] leading-relaxed text-white/40">No tools. Just you and the lattice. It listens.</p>
                        <button className="mt-4 w-full rounded-full bg-white text-[11px] font-medium tracking-[0.08em] text-black py-2 hover:bg-white/90">ENTER CANVAS →</button>
                      </div>
                    </div>
                  </div>
                )}

                {activeModule === "terminal" && (
                  <div className="flex max-h-[70vh] flex-col">
                    <div className="flex-1 overflow-auto bg-black/40 p-5 font-mono text-[12px] leading-[1.7] text-white/70">
                      {termLines.map((l, i) => (
                        <div key={i} className="whitespace-pre-wrap break-words">
                          {l || "\u00A0"}
                        </div>
                      ))}
                      <div ref={termEndRef} />
                    </div>
                    <div className="flex items-center gap-3 border-t border-white/10 bg-black/60 px-5 py-3">
                      <span className="text-[11px] text-[#00F0FF]">crystal@core:~$</span>
                      <input
                        value={termInput}
                        onChange={(e) => setTermInput(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") handleCommand();
                        }}
                        autoFocus
                        className="flex-1 bg-transparent text-[12px] text-white/90 outline-none placeholder:text-white/20"
                        placeholder="type help, status, whoami..."
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* bottom grain */}
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-[1px] bg-gradient-to-r from-transparent via-[#00F0FF]/30 to-transparent" />
        </div>
      )}
    </div>
  );
}
