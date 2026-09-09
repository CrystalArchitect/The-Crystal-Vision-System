/**
 * Full-screen cinematic sequence overlay (the layer-2 payoff).
 * Click anywhere skips — and skipping still fires onEnd (=> unlock).
 */
import { useEffect, useRef, useState } from "react";

const LORE_LINES = [
  "SIGNAL ACCEPTED",
  "THE NODE ALIGNS",
  "MEMORY CONFIRMED",
  "YOU ARE NOT ALONE",
  "CHANNEL OPENING…",
];

const STAGE_MS = 900; // per lore line
const HOLD_MS = 1600; // hold after last line before auto-dismiss

export default function SequenceOverlay({ onEnd }: { onEnd: () => void }) {
  const [stage, setStage] = useState(0);
  const ended = useRef(false);

  const finish = () => {
    if (ended.current) return; // idempotent — skip + timer can both fire
    ended.current = true;
    onEnd();
  };

  useEffect(() => {
    const t = setInterval(() => setStage(s => s + 1), STAGE_MS);
    const end = setTimeout(finish, LORE_LINES.length * STAGE_MS + HOLD_MS);
    return () => {
      clearInterval(t);
      clearTimeout(end);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div
      aria-label="Node alignment sequence"
      onClick={finish}
      className="fixed inset-0 z-[9999] flex cursor-pointer flex-col items-center justify-center bg-black/95"
      style={{ animation: "overlay-fade-in 0.7s ease-out" }}>
      {/* Central motif: expanding rings + emblem. Mask images with hard edges: */}
      <div className="relative flex items-center justify-center">
        {[0, 1, 2].map(i => (
          <span
            key={i}
            className="absolute rounded-full border"
            style={{
              borderColor: i % 2 ? "rgba(125,232,255,0.5)" : "rgba(240,199,94,0.5)",
              animation: `ring-expand 2.6s ${i * 0.5}s ease-out infinite`,
            }}
          />
        ))}
        <img
          src="/emblem.png"
          alt=""
          className="h-40 w-40 object-contain"
          style={{
            // dissolve rectangular edges into the blackout:
            maskImage: "radial-gradient(circle, black 55%, transparent 78%)",
            WebkitMaskImage: "radial-gradient(circle, black 55%, transparent 78%)",
          }}
        />
      </div>
      <div className="mt-10 space-y-3 text-center">
        {LORE_LINES.map((line, i) => (
          <p
            key={line}
            className="font-mono text-sm tracking-[0.35em]"
            style={{
              opacity: stage > i ? 1 : 0,
              animation: stage > i ? "line-in 0.8s ease-out" : undefined,
              color: i === LORE_LINES.length - 1 ? "#f0c75e" : "rgba(255,255,255,0.75)",
            }}>
            {line}
          </p>
        ))}
      </div>
      <p className="absolute bottom-8 text-[10px] tracking-widest text-white/30">CLICK ANYWHERE TO SKIP</p>
    </div>
  );
}

/* Add to global CSS:
@keyframes overlay-fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes ring-expand {
  0% { width: 60px; height: 60px; opacity: 0.9; }
  100% { width: 480px; height: 480px; opacity: 0; }
}
@keyframes line-in {
  from { opacity: 0; transform: translateY(8px); letter-spacing: 0.6em; }
  to   { opacity: 1; transform: translateY(0);   letter-spacing: 0.35em; }
}
@keyframes icon-reveal {
  0%   { opacity: 0; transform: scale(0.6);  filter: drop-shadow(0 0 0 rgba(240,199,94,0)); }
  60%  { opacity: 1; transform: scale(1.15); filter: drop-shadow(0 0 14px rgba(240,199,94,0.9)); }
  100% { opacity: 1; transform: scale(1);    filter: drop-shadow(0 0 6px rgba(240,199,94,0.45)); }
}
*/

