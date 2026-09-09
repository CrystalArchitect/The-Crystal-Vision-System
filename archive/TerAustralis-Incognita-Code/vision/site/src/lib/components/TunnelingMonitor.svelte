<script>
  // Quantum tunneling barrier transmission coefficient calculator
  // Vision: protocol fiction metaphor for network latency barriers

  // Physical constants
  const hbar = 1.0546e-34; // reduced Planck constant (J·s)
  const m_e = 9.109e-31;   // electron mass (kg)
  const eV_to_J = 1.602e-19; // eV to joules conversion

  // Small Council Phase 2 reference parameters
  let V0 = 7.50;   // barrier potential (eV)
  let E = 1.05;    // particle energy (eV)
  let L = 0.65;    // barrier width (nm)

  // Calculated values
  $: V0_J = V0 * eV_to_J;
  $: E_J = E * eV_to_J;
  $: L_m = L * 1e-9;

  $: kappa = Math.sqrt(2 * m_e * (V0_J - E_J)) / hbar;
  $: kappa_L = kappa * L_m;
  $: sinh_kL = Math.sinh(kappa_L);
  $: sinh2_kL = sinh_kL * sinh_kL;

  $: denominator = 1 + (V0 * V0 * sinh2_kL) / (4 * E * V0 * (V0 - E));
  $: T = denominator > 0 ? 1 / denominator : 0;

  $: T_scientific = T.toExponential(4);
  $: probability_inv = T > 0 ? (1 / T).toExponential(2) : 'infinite';

  // Barrier visualization: wave function amplitude decay
  $: barrierPoints = (() => {
    const points = [];
    for (let i = 0; i <= 100; i++) {
      const x_frac = i / 100;
      const x_m = x_frac * L_m;
      // Amplitude inside barrier decays as exp(-κx)
      const amplitude = Math.exp(-kappa * x_m);
      points.push({ x: x_frac * 200, y: 150 - amplitude * 100, amp: amplitude });
    }
    return points;
  })();

  // Energy level indicator
  $: barrierHeight = 150 - (V0 / (V0 + 2)) * 120; // normalize to viewbox
  $: energyLine = 150 - (E / (V0 + 2)) * 120;
</script>

<div class="monitor">
  <div class="header">
    <h3>Tunneling Barrier Monitor</h3>
    <p class="subtitle">Transmission probability across latency barrier (Vision framework)</p>
  </div>

  <div class="controls">
    <div class="control-group">
      <label for="v0">V₀ (barrier potential, eV)</label>
      <input type="range" id="v0" bind:value={V0} min="1" max="15" step="0.1" />
      <span class="value">{V0.toFixed(2)}</span>
    </div>

    <div class="control-group">
      <label for="e">E (particle energy, eV)</label>
      <input type="range" id="e" bind:value={E} min="0.1" max="14" step="0.05" />
      <span class="value">{E.toFixed(2)}</span>
    </div>

    <div class="control-group">
      <label for="l">L (barrier width, nm)</label>
      <input type="range" id="l" bind:value={L} min="0.1" max="2.0" step="0.05" />
      <span class="value">{L.toFixed(2)}</span>
    </div>
  </div>

  <div class="visualization">
    <svg viewBox="0 0 400 300" role="img" aria-labelledby="barrier-title barrier-desc">
      <title id="barrier-title">Quantum tunneling barrier visualization</title>
      <desc id="barrier-desc">Left: incident wave approaching barrier. Center: barrier potential (shaded) with decaying wave amplitude. Right: transmitted wave emerging.</desc>

      <defs>
        <linearGradient id="barrier-grad" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="var(--barrier-accent)" stopOpacity="0.3" />
          <stop offset="100%" stopColor="var(--barrier-accent)" stopOpacity="0.05" />
        </linearGradient>
      </defs>

      <!-- Barrier region (V₀) -->
      <rect x="80" y={barrierHeight} width="200" height={150 - barrierHeight} fill="url(#barrier-grad)" stroke="var(--barrier-accent)" strokeWidth="1" />
      <text x="180" y="40" textAnchor="middle" class="label-barrier">V₀ = {V0.toFixed(2)} eV</text>

      <!-- Energy level of particle -->
      <line x1="0" x2="400" y1={energyLine} y2={energyLine} stroke="var(--barrier-energy)" strokeDasharray="4 4" strokeWidth="1.5" />
      <text x="395" y={energyLine - 8} textAnchor="end" class="label-energy">E = {E.toFixed(2)} eV</text>

      <!-- Wave function decay inside barrier -->
      <polyline points={barrierPoints.map(p => `${p.x},${p.y}`).join(' ')} fill="none" stroke="var(--barrier-wave)" strokeWidth="2" />

      <!-- Incident wave (left of barrier) -->
      <path d="M 20 150 Q 30 130 40 150 Q 50 170 60 150 Q 70 130 80 150" fill="none" stroke="var(--barrier-wave)" strokeWidth="2" opacity="0.7" />

      <!-- Transmitted wave (right of barrier, attenuated) -->
      <path d="M 280 {energyLine} Q 290 {energyLine - 15 * T * 1e7} 300 {energyLine} Q 310 {energyLine + 15 * T * 1e7} 320 {energyLine}" fill="none" stroke="var(--barrier-wave)" strokeWidth="2" opacity={Math.min(T * 1e7, 0.5)} />

      <!-- Axis labels -->
      <text x="40" y="290" textAnchor="middle" class="label-axis">Incident</text>
      <text x="180" y="290" textAnchor="middle" class="label-axis">Barrier</text>
      <text x="320" y="290" textAnchor="middle" class="label-axis">Transmitted</text>
    </svg>
  </div>

  <div class="results">
    <div class="result-row">
      <span class="label">Decay constant (κ):</span>
      <span class="value">{(kappa / 1e10).toExponential(4)} m⁻¹</span>
    </div>

    <div class="result-row">
      <span class="label">Decay exponent (κL):</span>
      <span class="value">{kappa_L.toFixed(4)}</span>
    </div>

    <div class="result-row">
      <span class="label">sinh(κL):</span>
      <span class="value">{sinh_kL.toExponential(4)}</span>
    </div>

    <div class="result-row">
      <span class="label">sinh²(κL):</span>
      <span class="value">{sinh2_kL.toExponential(4)}</span>
    </div>

    <div class="divider"></div>

    <div class="result-row prominent">
      <span class="label">Transmission coefficient (T):</span>
      <span class="value transmission">{T_scientific}</span>
    </div>

    <div class="result-row prominent">
      <span class="label">Probability (1 in ___)</span>
      <span class="value probability">1 in {probability_inv}</span>
    </div>
  </div>

  <div class="footer">
    <p class="disclaimer">
      <strong>Vision framework:</strong> This is a metaphorical application of quantum tunneling to network latency barriers.
      <strong>Not a measurement.</strong> See <code>quantum-tunneling-barrier.md</code> for full methodology.
    </p>
  </div>
</div>

<style>
  .monitor {
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 24px;
    background: var(--monitor-bg);
    border: 1px solid var(--monitor-border);
    border-radius: 8px;
    font-family: var(--font-body, system-ui, sans-serif);
    color: var(--monitor-text);
  }

  .header {
    display: flex;
    flex-direction: column;
    gap: 6px;
    border-bottom: 1px solid var(--monitor-border);
    padding-bottom: 12px;
  }

  .header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: var(--monitor-title);
  }

  .subtitle {
    margin: 0;
    font-size: 12px;
    color: var(--monitor-muted);
    font-variant-numeric: tabular-nums;
  }

  .controls {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .control-group {
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 12px;
    align-items: center;
  }

  .control-group label {
    font-size: 13px;
    font-weight: 500;
    color: var(--monitor-label);
  }

  .control-group input[type="range"] {
    width: 100%;
    min-width: 150px;
    accent-color: var(--barrier-accent);
  }

  .control-group .value {
    font-size: 13px;
    font-variant-numeric: tabular-nums;
    color: var(--monitor-muted);
    min-width: 50px;
    text-align: right;
  }

  .visualization {
    width: 100%;
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--monitor-viz-bg);
    border: 1px solid var(--monitor-border);
    border-radius: 4px;
    padding: 12px;
  }

  .visualization svg {
    width: 100%;
    height: auto;
    max-width: 100%;
  }

  .label-barrier,
  .label-energy,
  .label-axis {
    font-size: 11px;
    font-weight: 500;
    fill: var(--monitor-label);
    letter-spacing: 0.05em;
  }

  .results {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 12px;
    background: var(--monitor-results-bg);
    border-radius: 4px;
    border: 1px solid var(--monitor-border);
  }

  .result-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
  }

  .result-row.prominent {
    padding: 8px;
    background: var(--monitor-highlight-bg);
    border-radius: 3px;
    border-left: 3px solid var(--barrier-accent);
  }

  .result-row .label {
    font-size: 12px;
    font-weight: 500;
    color: var(--monitor-label);
    flex-shrink: 0;
  }

  .result-row .value {
    font-size: 13px;
    font-variant-numeric: tabular-nums;
    color: var(--monitor-value);
    font-family: var(--font-mono, monospace);
    text-align: right;
  }

  .result-row .value.transmission {
    color: var(--barrier-accent);
    font-weight: 600;
    font-size: 14px;
  }

  .result-row .value.probability {
    color: var(--barrier-accent);
    font-weight: 500;
  }

  .divider {
    height: 1px;
    background: var(--monitor-border);
    margin: 4px 0;
  }

  .footer {
    border-top: 1px solid var(--monitor-border);
    padding-top: 12px;
  }

  .disclaimer {
    margin: 0;
    font-size: 11px;
    color: var(--monitor-muted);
    line-height: 1.5;
  }

  .disclaimer code {
    background: var(--monitor-code-bg);
    padding: 2px 4px;
    border-radius: 2px;
    font-family: var(--font-mono, monospace);
    font-size: 10px;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --monitor-bg: #0f1419;
      --monitor-border: #2a3238;
      --monitor-text: #e0e6ed;
      --monitor-title: #f0f4fa;
      --monitor-label: #a8b2c1;
      --monitor-value: #b8c5d6;
      --monitor-muted: #7a8494;
      --monitor-viz-bg: #131820;
      --monitor-results-bg: #0a0d12;
      --monitor-highlight-bg: #1a2332;
      --monitor-code-bg: #1e2530;
      --barrier-accent: #4a9eff;
      --barrier-energy: #ff7b42;
      --barrier-wave: #8b5cf6;
    }
  }

  @media (prefers-color-scheme: light) {
    :root {
      --monitor-bg: #f8f9fb;
      --monitor-border: #d4d8df;
      --monitor-text: #1a1f2e;
      --monitor-title: #0f1419;
      --monitor-label: #5a6372;
      --monitor-value: #2a3038;
      --monitor-muted: #8a9199;
      --monitor-viz-bg: #ffffff;
      --monitor-results-bg: #f3f5f8;
      --monitor-highlight-bg: #eff3f8;
      --monitor-code-bg: #f0f2f6;
      --barrier-accent: #0066cc;
      --barrier-energy: #cc5500;
      --barrier-wave: #7c3aed;
    }
  }

  @media (max-width: 640px) {
    .monitor {
      padding: 16px;
      gap: 16px;
    }

    .control-group {
      grid-template-columns: 1fr;
      gap: 8px;
    }

    .control-group label {
      grid-column: 1;
    }

    .control-group input[type="range"] {
      grid-column: 1;
    }

    .control-group .value {
      grid-column: 1;
      text-align: left;
    }
  }
</style>

<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
