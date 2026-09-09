<!-- DRAFT demo UI — decorative tunneling metaphor, not operational security tooling.
     Captured 2026-09-05 from chat paste. Requires Svelte + Tailwind-like utility classes. -->
<script>
  import { onMount } from 'svelte';

  // Core Physics Inputs (metaphor / demo only)
  let V0 = 5.0; // Firewall potential energy barrier (eV)
  let E = 1.25; // Data packet metadata energy (eV)
  let L = 0.5;  // Logic gate barrier depth (nm)

  const hbar = 1.0545718e-34; // J·s
  const m = 9.1093837e-31;    // kg (electron mass)
  const eV_to_J = 1.6021766e-19;

  $: kappa = Math.sqrt(2 * m * (V0 - E) * eV_to_J) / hbar;
  $: kappa_L = kappa * (L * 1e-9);
  $: sinh_kL = Math.sinh(kappa_L);
  $: T = 1 / (1 + (Math.pow(V0, 2) * Math.pow(sinh_kL, 2)) / (4 * E * (V0 - E)));
  $: decayFactor = Math.exp(-2 * kappa_L);

  $: points = Array.from({ length: 51 }, (_, i) => {
    let x_nm = (L * i) / 50;
    let current_kappa_x = kappa * (x_nm * 1e-9);
    let amplitude = Math.exp(-current_kappa_x);
    return { x: x_nm, y: amplitude };
  });
</script>

<main class="p-6 max-w-xl mx-auto bg-slate-900 text-slate-100 rounded-xl border border-slate-800 shadow-2xl">
  <h2 class="text-xl font-mono text-cyan-400 mb-4 border-b border-slate-800 pb-2">Ξ.Ξ.Λ.Τ // Tunneling Decay Tracker</h2>

  <div class="space-y-4 mb-6 text-sm font-mono">
    <div>
      <label class="block text-slate-400">Firewall Barrier Potential (V₀): {V0.toFixed(2)} eV</label>
      <input type="range" min="1.5" max="10.0" step="0.1" bind:value={V0} class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-400" />
    </div>
    <div>
      <label class="block text-slate-400">Packet Payload Energy (E): {E.toFixed(2)} eV</label>
      <input type="range" min="0.1" max={V0 - 0.1} step="0.1" bind:value={E} class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-400" />
    </div>
  </div>

  <div class="grid grid-cols-2 gap-4 mb-6 p-4 bg-slate-950 border border-slate-800 rounded-lg font-mono text-xs">
    <div>
      <span class="text-slate-500 block">TRANSMISSION COEFF. (T)</span>
      <span class="text-cyan-400 font-bold text-sm">{(T * 100).toFixed(5)}%</span>
    </div>
    <div>
      <span class="text-slate-500 block">BASE LOSS FACTOR (e⁻²κL)</span>
      <span class="text-rose-400 font-bold text-sm">{decayFactor.toExponential(4)}</span>
    </div>
  </div>

  <div class="relative bg-slate-950 p-2 border border-slate-800 rounded-lg">
    <div class="text-[10px] font-mono text-slate-500 absolute top-2 left-2">Wave Amplitude ψ(x)</div>
    <svg viewBox="0 0 500 200" class="w-full h-40 stroke-cyan-400 fill-none stroke-[2]">
      <line x1="0" y1="180" x2="500" y2="180" class="stroke-slate-800 stroke-[1]" />
      <line x1="0" y1="20" x2="500" y2="20" class="stroke-slate-800 stroke-[1]" />
      <path d="M {points.map((p, i) => `${(i * 10)},${180 - p.y * 160}`).join(' L ')}" />
      <circle cx="0" cy="20" r="4" class="fill-cyan-400 stroke-none" />
      <circle cx="500" cy={180 - points[50].y * 160} r="4" class="fill-rose-400 stroke-none" />
    </svg>
    <div class="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
      <span>x = 0 nm (Entry Node)</span>
      <span>x = {L} nm (Exit Gateway)</span>
    </div>
  </div>
</main>
