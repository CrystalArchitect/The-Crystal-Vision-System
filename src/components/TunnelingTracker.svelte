<script>
  let V0 = 7.50;
  let E = 1.05;
  let L = 0.65;
  let repetitionRate = 25;

  const hbar = 1.0545718e-34;
  const m = 9.1093837e-31;
  const eV_to_J = 1.6021766e-19;

  $: kappa = Math.sqrt(2 * m * (V0 - E) * eV_to_J) / hbar;
  $: kappa_L = kappa * (L * 1e-9);
  $: sinh_kL = Math.sinh(kappa_L);
  $: T = 1 / (1 + (Math.pow(V0, 2) * Math.pow(sinh_kL, 2)) / (4 * E * (V0 - E)));
  $: decayFactor = Math.exp(-2 * kappa_L);
  $: netThroughput = T * (repetitionRate * 1000);
</script>

<div class="tracker-node" style="font-family: monospace; background: #020617; color: #f8fafc; padding: 1.5rem; border: 1px solid #1e293b; border-radius: 0.75rem;">
  <div style="border-bottom: 1px solid #1e293b; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    <span style="color: #22d3ee; font-weight: bold;">[Ξ.Ξ.Λ.Τ] INTERNAL MONITOR</span>
  </div>

  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-size: 0.75rem; color: #94a3b8;">V0 (Barrier): {V0} eV</label>
    <input type="range" min="5.0" max="12.0" step="0.1" bind:value={V0} style="width: 100%;" />
  </div>

  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-size: 0.75rem; color: #94a3b8;">E (Energy): {E} eV</label>
    <input type="range" min="0.5" max={V0 - 0.1} step="0.1" bind:value={E} style="width: 100%;" />
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; font-size: 0.875rem; background: #090d16; padding: 0.75rem; border-radius: 0.5rem;">
    <div>T_COEFF: <span style="color: #22d3ee;">{T.toExponential(4)}</span></div>
    <div>LOSS_FAC: <span style="color: #f43f5e;">{decayFactor.toExponential(4)}</span></div>
    <div style="grid-column: span 2; margin-top: 0.25rem;">THROUGHPUT: <span style="color: #10b981;">{netThroughput.toFixed(6)} packets/s</span></div>
  </div>
</div>
