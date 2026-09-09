<!-- DRAFT demo UI — Independent PoC framing. Metaphor physics only.
     "PoC-VALIDATED" badges are UI fiction, not live verification.
     Captured 2026-09-05. Location string generalized (privacy). -->
<script>
  let V0 = 5.0;
  let E = 1.25;
  let barrierDepth = 0.50;
  let repetitionRate = 12;
  let selectedSupplier = "All";

  const hbar = 1.0545718e-34;
  const m_eff = 9.1093837e-31;
  const eV_to_Joules = 1.6021766e-19;

  $: kappa = Math.sqrt(2 * m_eff * (V0 - E) * eV_to_Joules) / hbar;
  $: kappa_L = kappa * (barrierDepth * 1e-9);
  $: sinh_kL = Math.sinh(kappa_L);
  $: T_prob = 1 / (1 + (Math.pow(V0, 2) * Math.pow(sinh_kL, 2)) / (4 * E * (V0 - E)));
  $: basePowerLoss = Math.exp(-2 * kappa_L);
  $: adjustedThroughput = T_prob * (repetitionRate / 20);

  const suppliers = [
    { id: 'lynas', name: 'Lynas Rare Earths', tier: 1, focus: 'REE Extraction & Cracking' },
    { id: 'magellan', name: 'Magellan Aerospace', tier: 2, focus: 'Precision Components & Machining' },
    { id: 'liquid', name: 'Liquid Instruments', tier: 3, focus: 'FPGA Telemetry Signalling' },
    { id: 'ela', name: 'Equatorial Launch Australia', tier: 4, focus: 'Downstream Orbital Placement' }
  ];
</script>

<main class="p-6 max-w-2xl mx-auto bg-slate-950 text-slate-100 rounded-xl border border-slate-800 shadow-2xl font-mono text-sm">
  <header class="border-b border-slate-800 pb-3 mb-6 flex justify-between items-center">
    <div>
      <h1 class="text-lg font-bold text-cyan-400">Ξ.Ξ.Λ.Τ // Sovereign Node Matrix</h1>
      <p class="text-xs text-slate-500">Node: NSW // Independent PoC Array (demo)</p>
    </div>
    <span class="px-2 py-1 bg-cyan-950/50 border border-cyan-800 text-cyan-400 text-xs rounded">ONLINE</span>
  </header>

  <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
    <div class="space-y-4">
      <h3 class="text-xs uppercase text-slate-400 tracking-wider font-bold">1. Network Potential Inputs</h3>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Firewall Barrier Height (V₀): {V0.toFixed(2)} eV</label>
        <input type="range" min="2.0" max="10.0" step="0.1" bind:value={V0} class="w-full h-1 bg-slate-800 rounded appearance-none cursor-pointer accent-cyan-400" />
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Packet Momentum Energy (E): {E.toFixed(2)} eV</label>
        <input type="range" min="0.1" max={V0 - 0.1} step="0.1" bind:value={E} class="w-full h-1 bg-slate-800 rounded appearance-none cursor-pointer accent-cyan-400" />
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Logic Inspection Gate Depth (L): {barrierDepth.toFixed(2)} nm</label>
        <input type="range" min="0.10" max="1.50" step="0.05" bind:value={barrierDepth} class="w-full h-1 bg-slate-800 rounded appearance-none cursor-pointer accent-cyan-400" />
      </div>
    </div>

    <div class="space-y-4">
      <h3 class="text-xs uppercase text-slate-400 tracking-wider font-bold">2. Local Corridor Optimization</h3>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Burst Transmission Frequency: {repetitionRate} kHz</label>
        <input type="range" min="1" max="50" step="1" bind:value={repetitionRate} class="w-full h-1 bg-slate-800 rounded appearance-none cursor-pointer accent-emerald-400" />
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Active PoC Data Feed Filter</label>
        <select bind:value={selectedSupplier} class="w-full bg-slate-900 border border-slate-800 rounded p-2 text-xs text-slate-300 focus:outline-none focus:border-cyan-500">
          <option value="All">All Small Council Nodes</option>
          {#each suppliers as s}
            <option value={s.id}>Tier {s.tier} // {s.name}</option>
          {/each}
        </select>
      </div>
    </div>
  </section>

  <section class="grid grid-cols-3 gap-2 bg-slate-900 p-4 border border-slate-800 rounded-lg text-center mb-6">
    <div>
      <div class="text-[10px] text-slate-500 uppercase">Tunneling Prob. (T)</div>
      <div class="text-cyan-400 font-bold text-base mt-1">{(T_prob * 100).toExponential(4)}%</div>
    </div>
    <div>
      <div class="text-[10px] text-slate-500 uppercase">Power Loss Factor</div>
      <div class="text-rose-400 font-bold text-base mt-1">{basePowerLoss.toExponential(4)}</div>
    </div>
    <div>
      <div class="text-[10px] text-slate-500 uppercase">Net Throughput Score</div>
      <div class="text-emerald-400 font-bold text-base mt-1">{adjustedThroughput.toFixed(4)}</div>
    </div>
  </section>

  <section class="border-t border-slate-800 pt-4">
    <h3 class="text-xs uppercase text-slate-400 tracking-wider font-bold mb-3">Ecosystem Verification Pipeline Status (demo badges)</h3>
    <div class="space-y-2">
      {#each suppliers as s}
        {#if selectedSupplier === "All" || selectedSupplier === s.id}
          <div class="p-2 bg-slate-900/40 border border-slate-800/80 rounded flex justify-between items-center text-xs">
            <div>
              <span class="font-bold text-slate-300">{s.name}</span>
              <span class="text-slate-500 block text-[11px]">Focus: {s.focus}</span>
            </div>
            <div class="text-right">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950/40 border border-amber-800 text-amber-400">
                PoC-SCOPED (draft)
              </span>
              <span class="text-slate-600 block text-[9px] mt-1">Demo loss tag: {(basePowerLoss * s.tier).toExponential(2)}</span>
            </div>
          </div>
        {/if}
      {/each}
    </div>
  </section>
</main>
