// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

const state = {
  epoch: "sister-2-danube-gate",
  region: "budapest-starline",
  layers: { water: true, energy: true, data: false, mobility: true },
  pipeStep: 0,
  credits: 1240.5,
  coreBalance: 42.8,
  staked: 1000,
  nodes: [],
  receipts: [],
  selectedNode: null,
  burnRate: 100,
  mintAlpha: 0.1,
  simMint: 0,
};

const NODES = [
  { id: "n1", name: "Budapest Hub", x: 0.5, y: 0.45, stake: 5000, classes: ["mobility", "energy"] },
  { id: "n2", name: "Vienna Edge", x: 0.35, y: 0.35, stake: 2000, classes: ["energy"] },
  { id: "n3", name: "Danube Sensor", x: 0.55, y: 0.55, stake: 1000, classes: ["water"] },
  { id: "n4", name: "Bratislava Relay", x: 0.42, y: 0.5, stake: 1500, classes: ["data", "mobility"] },
  { id: "n5", name: "User Node", x: 0.65, y: 0.4, stake: 0, classes: [] },
];

const ROUTES = [
  { dest: "Vienna", time: "0h 52m", status: "live" },
  { dest: "Bratislava", time: "1h 08m", status: "live" },
  { dest: "Berlin", time: "2h 54m", status: "beta" },
  { dest: "Belgrade", time: "3h 12m", status: "planned" },
];

function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2800);
}

// Twin animation runs as a single loop; guard so re-entering the panel
// never stacks a second requestAnimationFrame chain.
let twinRunning = false;

function showPanel(id) {
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  const panel = document.getElementById("panel-" + id);
  if (panel) panel.classList.add("active");
  const btn = document.querySelector(`[data-panel="${id}"]`);
  if (btn) btn.classList.add("active");
  if (id === "twin" && !twinRunning) {
    twinRunning = true;
    requestAnimationFrame(drawTwin);
  }
  if (id === "mesh") drawMesh();
}

function initNav() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => showPanel(btn.dataset.panel));
  });
}

function animateStats() {
  const el = document.getElementById("stat-nodes");
  if (!el) return;
  let n = 0;
  const target = 847;
  const iv = setInterval(() => {
    n += Math.ceil((target - n) / 12);
    if (n >= target) { n = target; clearInterval(iv); }
    el.textContent = n.toLocaleString();
  }, 40);
}

// Twin canvas
let twinParticles = [];
function seedParticles() {
  twinParticles = [];
  for (let i = 0; i < 80; i++) {
    twinParticles.push({
      x: Math.random(), y: Math.random(),
      vx: (Math.random() - 0.5) * 0.002,
      vy: (Math.random() - 0.5) * 0.002,
      layer: ["water", "energy", "data", "mobility"][Math.floor(Math.random() * 4)]
    });
  }
}

function drawTwin() {
  const c = document.getElementById("twinCanvas");
  if (!c) return;
  const ctx = c.getContext("2d");
  const w = c.width = c.offsetWidth * devicePixelRatio;
  const h = c.height = c.offsetHeight * devicePixelRatio;
  ctx.scale(devicePixelRatio, devicePixelRatio);
  const W = c.offsetWidth, H = c.offsetHeight;
  ctx.fillStyle = "#050810";
  ctx.fillRect(0, 0, W, H);

  // Danube ribbon
  if (state.layers.water) {
    ctx.strokeStyle = "rgba(34, 211, 238, 0.5)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let x = 0; x <= W; x += 8) {
      const y = H * 0.55 + Math.sin(x * 0.02) * 25;
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // Hub glow
  if (state.layers.mobility) {
    const hx = W * 0.5, hy = H * 0.45;
    const g = ctx.createRadialGradient(hx, hy, 0, hx, hy, 80);
    g.addColorStop(0, "rgba(251, 191, 36, 0.35)");
    g.addColorStop(1, "transparent");
    ctx.fillStyle = g;
    ctx.fillRect(hx - 80, hy - 80, 160, 160);
    ctx.fillStyle = "#fbbf24";
    ctx.font = "11px system-ui";
    ctx.fillText("Starline Budapest", hx - 48, hy - 90);
  }

  // Energy grid
  if (state.layers.energy) {
    ctx.strokeStyle = "rgba(167, 139, 250, 0.35)";
    ctx.lineWidth = 1;
    for (let i = 0; i < 6; i++) {
      ctx.beginPath();
      ctx.moveTo(W * 0.2, H * (0.2 + i * 0.12));
      ctx.lineTo(W * 0.8, H * (0.25 + i * 0.1));
      ctx.stroke();
    }
  }

  // Data pulses
  if (state.layers.data) {
    twinParticles.forEach(p => {
      if (p.layer !== "data") return;
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > 1) p.vx *= -1;
      if (p.y < 0 || p.y > 1) p.vy *= -1;
      ctx.fillStyle = "rgba(34, 211, 238, 0.8)";
      ctx.beginPath();
      ctx.arc(p.x * W, p.y * H, 3, 0, Math.PI * 2);
      ctx.fill();
    });
  } else {
    twinParticles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
    });
  }

  requestAnimationFrame(drawTwin);
}

function bindLayerToggles() {
  document.querySelectorAll("[data-layer]").forEach(el => {
    el.addEventListener("click", () => {
      const layer = el.dataset.layer;
      state.layers[layer] = !state.layers[layer];
      el.classList.toggle("on", state.layers[layer]);
      toast(layer + " layer " + (state.layers[layer] ? "on" : "off"));
    });
  });
}

const PIPE_DATA = [
  { step: "decode", label: "DECODE", obj: { schema: "crystal.twin.event/1", class: "energy.kwh", value: "12.4", source_did: "did:crystal:hub-bud" } },
  { step: "ingest", label: "INGEST", obj: { partition: "h3:8abe", stored: true, latency_ms: 142 } },
  { step: "twin", label: "TWIN", obj: { flow_id: "energy.danube-hub", layer: "energy", aggregate_1h: 124.5 } },
  { step: "receipt", label: "RECEIPT", obj: { schema: "crystal.service.receipt/1", credit_debit: "12.45", status: "pending" } },
  { step: "econ", label: "ECON", obj: { burn: null, mint_preview: 1.24, credits_remaining: state.credits } },
  { step: "upgrade", label: "UPGRADE", obj: { epoch: state.epoch, schema_ok: true, timelock: "48h" } },
];

function renderPipeline() {
  const container = document.getElementById("pipelineSteps");
  const jsonEl = document.getElementById("pipelineJson");
  if (!container) return;
  container.innerHTML = PIPE_DATA.map((p, i) => {
    let cls = "pipe-step";
    if (i === state.pipeStep) cls += " active";
    if (i < state.pipeStep) cls += " done";
    return `<div class="${cls}" data-idx="${i}"><h4>${p.label}</h4><p>Click</p></div>`;
  }).join("");
  container.querySelectorAll(".pipe-step").forEach(el => {
    el.addEventListener("click", () => {
      state.pipeStep = parseInt(el.dataset.idx, 10);
      renderPipeline();
      if (jsonEl) jsonEl.textContent = JSON.stringify(PIPE_DATA[state.pipeStep].obj, null, 2);
      logEvent("pipeline", "Step " + PIPE_DATA[state.pipeStep].label);
    });
  });
  if (jsonEl) jsonEl.textContent = JSON.stringify(PIPE_DATA[state.pipeStep].obj, null, 2);
}

function runPipelineAuto() {
  state.pipeStep = 0;
  renderPipeline();
  const iv = setInterval(() => {
    if (state.pipeStep >= PIPE_DATA.length - 1) {
      clearInterval(iv);
      toast("Pipeline complete → receipt mint-eligible");
      return;
    }
    state.pipeStep++;
    renderPipeline();
  }, 900);
}

function updateEconSim() {
  const burn = parseFloat(document.getElementById("sliderBurn")?.value || state.burnRate);
  const alpha = parseFloat(document.getElementById("sliderAlpha")?.value || state.mintAlpha);
  const burnAmt = parseFloat(document.getElementById("inputBurnCore")?.value || 1);
  state.burnRate = burn;
  state.mintAlpha = alpha;
  const creditsOut = burnAmt * burn * 0.98;
  const serviceVal = parseFloat(document.getElementById("inputService")?.value || 100);
  state.simMint = alpha * serviceVal * 1.1;
  const elC = document.getElementById("simCredits");
  const elM = document.getElementById("simMint");
  if (elC) elC.textContent = creditsOut.toFixed(2);
  if (elM) elM.textContent = state.simMint.toFixed(3);
}

function doBurn() {
  const amt = parseFloat(document.getElementById("inputBurnCore")?.value || 1);
  state.coreBalance = Math.max(0, state.coreBalance - amt);
  state.credits += amt * state.burnRate * 0.98;
  document.getElementById("walletCore").textContent = state.coreBalance.toFixed(2);
  document.getElementById("walletCredits").textContent = state.credits.toFixed(2);
  toast("Burned " + amt + " CORE → credits");
  logEvent("econ", "burn " + amt);
}

function drawMesh() {
  const svg = document.getElementById("meshSvg");
  if (!svg) return;
  const w = 600, h = 280;
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
  const links = [[0,1],[0,2],[0,3],[1,3],[3,4]];
  let html = "";
  links.forEach(([a,b]) => {
    const n1 = NODES[a], n2 = NODES[b];
    html += `<line x1="${n1.x*w}" y1="${n1.y*h}" x2="${n2.x*w}" y2="${n2.y*h}" stroke="rgba(34,211,238,0.25)" stroke-width="1"/>`;
  });
  NODES.forEach((n, i) => {
    const sel = state.selectedNode === n.id ? ' stroke="#fbbf24" stroke-width="3"' : ' stroke="#22d3ee" stroke-width="1"';
    html += `<circle class="node-circle" data-id="${n.id}" cx="${n.x*w}" cy="${n.y*h}" r="14" fill="#1a2540"${sel}/>`;
    html += `<text x="${n.x*w}" y="${n.y*h+28}" fill="#94a3b8" font-size="10" text-anchor="middle">${n.name}</text>`;
  });
  svg.innerHTML = html;
  svg.querySelectorAll(".node-circle").forEach(c => {
    c.addEventListener("click", () => {
      state.selectedNode = c.dataset.id;
      const n = NODES.find(x => x.id === state.selectedNode);
      document.getElementById("nodeDetail").textContent = JSON.stringify(n, null, 2);
      drawMesh();
    });
  });
}

function addReceipt() {
  const r = {
    id: "rcpt-" + Date.now().toString(36),
    class: document.getElementById("rcptClass")?.value || "energy.kwh",
    qty: document.getElementById("rcptQty")?.value || "10",
    status: "pending"
  };
  state.receipts.unshift(r);
  renderReceipts();
  toast("Receipt created (pending consumer confirm)");
}

function confirmReceipt(id) {
  const r = state.receipts.find(x => x.id === id);
  if (r) { r.status = "confirmed"; renderReceipts(); toast("Confirmed → mint queued"); }
}

function renderReceipts() {
  const tbody = document.getElementById("receiptTable");
  if (!tbody) return;
  tbody.innerHTML = state.receipts.slice(0, 8).map(r =>
    `<tr><td>${r.id}</td><td>${r.class}</td><td>${r.qty}</td><td><span class="receipt-status ${r.status}">${r.status}</span></td>
    <td>${r.status === "pending" ? `<button class="btn" onclick="confirmReceipt('${r.id}')">Confirm</button>` : "—"}</td></tr>`
  ).join("") || "<tr><td colspan='5'>No receipts — create one</td></tr>";
}

function logEvent(cat, msg) {
  const el = document.getElementById("eventLog");
  if (!el) return;
  const line = document.createElement("div");
  line.className = "line-info";
  line.textContent = `[${new Date().toLocaleTimeString()}] ${cat}: ${msg}`;
  el.prepend(line);
}

function bindLayersStack() {
  document.querySelectorAll(".layer-bar").forEach(bar => {
    bar.addEventListener("click", () => bar.classList.toggle("expanded"));
  });
}

function openWalletModal() {
  document.getElementById("modalWallet").classList.add("open");
}

function closeModals() {
  document.querySelectorAll(".modal-backdrop").forEach(m => m.classList.remove("open"));
}

function initRoutes() {
  const ul = document.getElementById("routeList");
  if (!ul) return;
  ul.innerHTML = ROUTES.map(r =>
    `<li><span>${r.dest}</span><span class="time">${r.time} <small>(${r.status})</small></span></li>`
  ).join("");
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  seedParticles();
  bindLayerToggles();
  renderPipeline();
  updateEconSim();
  drawMesh();
  initRoutes();
  bindLayersStack();
  animateStats();
  showPanel("overview");

  document.getElementById("btnRunPipe")?.addEventListener("click", runPipelineAuto);
  document.getElementById("sliderBurn")?.addEventListener("input", updateEconSim);
  document.getElementById("sliderAlpha")?.addEventListener("input", updateEconSim);
  document.getElementById("inputBurnCore")?.addEventListener("input", updateEconSim);
  document.getElementById("inputService")?.addEventListener("input", updateEconSim);
  document.getElementById("btnBurn")?.addEventListener("click", doBurn);
  document.getElementById("btnAddReceipt")?.addEventListener("click", addReceipt);
  document.getElementById("btnWallet")?.addEventListener("click", openWalletModal);
  document.getElementById("btnCloseModal")?.addEventListener("click", closeModals);
  document.getElementById("epochSelect")?.addEventListener("change", e => {
    state.epoch = e.target.value;
    toast("Epoch: " + state.epoch);
  });

  window.confirmReceipt = confirmReceipt;
});
