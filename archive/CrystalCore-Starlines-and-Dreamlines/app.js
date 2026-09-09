/* Crystal Core interactive shell — complete demo UI (not production) */
const state = {
  epoch: "sister-2-danube-gate",
  region: "budapest-starline",
  layers: { water: true, energy: true, data: false, mobility: true },
  pipeStep: 0,
  credits: 1240.5,
  coreBalance: 42.8,
  staked: 1000,
  selectedNode: null,
  burnRate: 100,
  mintAlpha: 0.1,
  simMint: 0,
  receipts: [],
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

const PIPE_DATA = [
  {
    step: "decode",
    label: "DECODE",
    obj: {
      schema: "crystal.decode.candidate/1",
      class: "energy.kwh",
      value: "12.4",
      source_did: "did:crystal:hub-bud",
      hub: "starline-budapest",
    },
  },
  {
    step: "ingest",
    label: "INGEST",
    obj: { partition: "h3:8abe", stored: true, latency_ms: 142, policy: "governance_cap_ok" },
  },
  {
    step: "twin",
    label: "TWIN",
    obj: { flow_id: "energy.danube-hub", layer: "energy", aggregate_1h: 124.5 },
  },
  {
    step: "receipt",
    label: "RECEIPT",
    obj: {
      schema: "crystal.service.receipt/1",
      credit_debit: "12.45",
      credit_currency: "EUR-C",
      status: "pending",
    },
  },
  {
    step: "econ",
    label: "ECON",
    obj: { burn: null, mint_preview: 1.24, credits_remaining: 1240.5, mainnet: false },
  },
  {
    step: "upgrade",
    label: "UPGRADE",
    obj: { epoch: "sister-2-danube-gate", schema_ok: true, timelock: "48h", authority: "HOLD" },
  },
];

function toast(msg) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2800);
}

function logEvent(cat, msg) {
  const el = document.getElementById("eventLog");
  if (!el) return;
  const line = document.createElement("div");
  line.className = "line-info";
  line.textContent = `[${new Date().toLocaleTimeString()}] ${cat}: ${msg}`;
  el.prepend(line);
}

function clearLog() {
  const el = document.getElementById("eventLog");
  if (el) el.innerHTML = "";
}

function showPanel(id) {
  document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
  const panel = document.getElementById("panel-" + id);
  if (panel) panel.classList.add("active");
  const btn = document.querySelector(`.nav-btn[data-panel="${id}"]`);
  if (btn) btn.classList.add("active");
  if (id === "mesh") drawMesh();
  if (id === "receipts") renderReceipts();
}

function initNav() {
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => showPanel(btn.dataset.panel));
  });
  document.querySelectorAll("[data-go]").forEach((btn) => {
    btn.addEventListener("click", () => showPanel(btn.dataset.go));
  });
}

function animateStats() {
  const el = document.getElementById("stat-nodes");
  if (!el) return;
  let n = 0;
  const target = 847;
  const iv = setInterval(() => {
    n += Math.ceil((target - n) / 12);
    if (n >= target) {
      n = target;
      clearInterval(iv);
    }
    el.textContent = n.toLocaleString();
  }, 40);
  syncWalletUI();
}

let twinParticles = [];
function seedParticles() {
  twinParticles = [];
  for (let i = 0; i < 80; i++) {
    twinParticles.push({
      x: Math.random(),
      y: Math.random(),
      vx: (Math.random() - 0.5) * 0.002,
      vy: (Math.random() - 0.5) * 0.002,
      layer: ["water", "energy", "data", "mobility"][Math.floor(Math.random() * 4)],
    });
  }
}

function drawTwin() {
  const c = document.getElementById("twinCanvas");
  if (!c) {
    requestAnimationFrame(drawTwin);
    return;
  }
  if (!document.getElementById("panel-twin")?.classList.contains("active")) {
    requestAnimationFrame(drawTwin);
    return;
  }
  const dpr = window.devicePixelRatio || 1;
  const W = c.offsetWidth;
  const H = c.offsetHeight;
  if (c.width !== W * dpr || c.height !== H * dpr) {
    c.width = W * dpr;
    c.height = H * dpr;
  }
  const ctx = c.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = "#050810";
  ctx.fillRect(0, 0, W, H);

  ctx.strokeStyle = "rgba(34, 211, 238, 0.06)";
  for (let x = 0; x < W; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, H);
    ctx.stroke();
  }

  if (state.layers.water) {
    ctx.strokeStyle = "rgba(34, 211, 238, 0.55)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let x = 0; x <= W; x += 6) {
      const y = H * 0.55 + Math.sin(x * 0.02 + Date.now() * 0.001) * 22;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.fillStyle = "rgba(34, 211, 238, 0.7)";
    ctx.font = "11px system-ui";
    ctx.fillText("Danube flow layer", 16, H * 0.55 - 28);
  }

  if (state.layers.mobility) {
    const hx = W * 0.5;
    const hy = H * 0.42;
    const g = ctx.createRadialGradient(hx, hy, 0, hx, hy, 90);
    g.addColorStop(0, "rgba(251, 191, 36, 0.4)");
    g.addColorStop(1, "transparent");
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(hx, hy, 90, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#fbbf24";
    ctx.font = "bold 12px system-ui";
    ctx.fillText("Starline Budapest", hx - 52, hy - 98);
    [
      [0.35, 0.32],
      [0.42, 0.5],
      [0.65, 0.35],
    ].forEach(([x, y]) => {
      ctx.strokeStyle = "rgba(251, 191, 36, 0.35)";
      ctx.beginPath();
      ctx.moveTo(hx, hy);
      ctx.lineTo(W * x, H * y);
      ctx.stroke();
    });
  }

  if (state.layers.energy) {
    ctx.strokeStyle = "rgba(167, 139, 250, 0.4)";
    ctx.lineWidth = 1;
    for (let i = 0; i < 6; i++) {
      ctx.beginPath();
      ctx.moveTo(W * 0.15, H * (0.18 + i * 0.12));
      ctx.lineTo(W * 0.85, H * (0.22 + i * 0.1));
      ctx.stroke();
    }
  }

  twinParticles.forEach((p) => {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < 0 || p.x > 1) p.vx *= -1;
    if (p.y < 0 || p.y > 1) p.vy *= -1;
    if (!state.layers[p.layer]) return;
    const colors = {
      water: "rgba(34, 211, 238, 0.85)",
      energy: "rgba(167, 139, 250, 0.85)",
      data: "rgba(52, 211, 153, 0.85)",
      mobility: "rgba(251, 191, 36, 0.85)",
    };
    ctx.fillStyle = colors[p.layer] || "#fff";
    ctx.beginPath();
    ctx.arc(p.x * W, p.y * H, 2.5, 0, Math.PI * 2);
    ctx.fill();
  });

  requestAnimationFrame(drawTwin);
}

function bindLayerToggles() {
  document.querySelectorAll("[data-layer]").forEach((el) => {
    const layer = el.dataset.layer;
    el.classList.toggle("on", !!state.layers[layer]);
    el.addEventListener("click", () => {
      state.layers[layer] = !state.layers[layer];
      el.classList.toggle("on", state.layers[layer]);
      toast(layer + " layer " + (state.layers[layer] ? "on" : "off"));
      logEvent("twin", layer + " → " + state.layers[layer]);
    });
  });
}

function renderPipeline() {
  const container = document.getElementById("pipelineSteps");
  const jsonEl = document.getElementById("pipelineJson");
  if (!container) return;
  container.innerHTML = PIPE_DATA.map((p, i) => {
    let cls = "pipe-step";
    if (i === state.pipeStep) cls += " active";
    if (i < state.pipeStep) cls += " done";
    return `<div class="${cls}" data-idx="${i}"><h4>${p.label}</h4><p>step ${i + 1}</p></div>`;
  }).join("");
  container.querySelectorAll(".pipe-step").forEach((el) => {
    el.addEventListener("click", () => {
      state.pipeStep = parseInt(el.dataset.idx, 10);
      renderPipeline();
      logEvent("pipeline", "Step " + PIPE_DATA[state.pipeStep].label);
    });
  });
  if (jsonEl) {
    const obj = { ...PIPE_DATA[state.pipeStep].obj };
    if (obj.credits_remaining !== undefined) obj.credits_remaining = state.credits;
    if (obj.epoch !== undefined) obj.epoch = state.epoch;
    jsonEl.textContent = JSON.stringify(obj, null, 2);
  }
}

function runPipelineAuto() {
  state.pipeStep = 0;
  renderPipeline();
  showPanel("pipeline");
  const iv = setInterval(() => {
    if (state.pipeStep >= PIPE_DATA.length - 1) {
      clearInterval(iv);
      toast("Pipeline complete → receipt mint-eligible");
      logEvent("pipeline", "complete → mint_eligible");
      // mirror into receipts table
      addReceiptFromPipeline();
      return;
    }
    state.pipeStep++;
    renderPipeline();
  }, 900);
}

function addReceiptFromPipeline() {
  state.receipts.unshift({
    id: "rcpt-" + Date.now().toString(36),
    class: "energy.kwh",
    qty: "12.4",
    status: "pending",
  });
  renderReceipts();
}

function addReceipt() {
  const r = {
    id: "rcpt-" + Date.now().toString(36),
    class: document.getElementById("rcptClass")?.value || "energy.kwh",
    qty: document.getElementById("rcptQty")?.value || "10",
    status: "pending",
  };
  state.receipts.unshift(r);
  renderReceipts();
  toast("Receipt created (pending consumer confirm)");
  logEvent("receipt", "pending " + r.id + " " + r.class);
}

function confirmReceipt(id) {
  const r = state.receipts.find((x) => x.id === id);
  if (r) {
    r.status = "confirmed";
    renderReceipts();
    toast("Confirmed → mint queued (demo)");
    logEvent("receipt", "confirmed " + id);
  }
}

function renderReceipts() {
  const tbody = document.getElementById("receiptTable");
  if (!tbody) return;
  tbody.innerHTML =
    state.receipts
      .slice(0, 12)
      .map(
        (r) =>
          `<tr>
            <td class="mono">${r.id}</td>
            <td>${r.class}</td>
            <td>${r.qty}</td>
            <td><span class="receipt-status ${r.status}">${r.status}</span></td>
            <td>${
              r.status === "pending"
                ? `<button class="btn" type="button" data-confirm="${r.id}">Confirm</button>`
                : "—"
            }</td>
          </tr>`
      )
      .join("") || "<tr><td colspan='5'>No receipts — create one</td></tr>";

  tbody.querySelectorAll("[data-confirm]").forEach((btn) => {
    btn.addEventListener("click", () => confirmReceipt(btn.dataset.confirm));
  });
}

function updateEconSim() {
  const burn = parseFloat(document.getElementById("sliderBurn")?.value || state.burnRate);
  const alpha = parseFloat(document.getElementById("sliderAlpha")?.value || state.mintAlpha);
  const burnAmt = parseFloat(document.getElementById("inputBurnCore")?.value || 1);
  const serviceVal = parseFloat(document.getElementById("inputService")?.value || 100);
  state.burnRate = burn;
  state.mintAlpha = alpha;
  const creditsOut = burnAmt * burn * 0.98;
  state.simMint = alpha * serviceVal * 1.1;
  const elC = document.getElementById("simCredits");
  const elM = document.getElementById("simMint");
  const lb = document.getElementById("lblBurn");
  const la = document.getElementById("lblAlpha");
  if (elC) elC.textContent = creditsOut.toFixed(2);
  if (elM) elM.textContent = state.simMint.toFixed(3);
  if (lb) lb.textContent = String(burn);
  if (la) la.textContent = alpha.toFixed(2);
}

function doBurn() {
  const amt = parseFloat(document.getElementById("inputBurnCore")?.value || 1);
  if (amt > state.coreBalance) {
    toast("Insufficient CORE (demo wallet)");
    return;
  }
  state.coreBalance = Math.max(0, state.coreBalance - amt);
  state.credits += amt * state.burnRate * 0.98;
  syncWalletUI();
  toast("Burned " + amt + " CORE → credits");
  logEvent("econ", "burn " + amt + " CORE @ R=" + state.burnRate);
  updateEconSim();
}

function syncWalletUI() {
  const map = {
    walletCore: state.coreBalance.toFixed(2),
    walletCredits: state.credits.toFixed(2),
    walletStaked: String(state.staked),
    modalCore: state.coreBalance.toFixed(2),
    modalCredits: state.credits.toFixed(2),
    modalStaked: String(state.staked),
  };
  Object.entries(map).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  });
  const sc = document.getElementById("stat-credits");
  const so = document.getElementById("stat-core");
  if (sc) sc.textContent = Math.round(state.credits).toLocaleString();
  if (so) so.textContent = state.coreBalance.toFixed(1);
}

function drawMesh() {
  const svg = document.getElementById("meshSvg");
  if (!svg) return;
  const w = 600;
  const h = 280;
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
  const links = [
    [0, 1],
    [0, 2],
    [0, 3],
    [1, 3],
    [3, 4],
    [1, 4],
  ];
  let html = "";
  links.forEach(([a, b]) => {
    const n1 = NODES[a];
    const n2 = NODES[b];
    html += `<line x1="${n1.x * w}" y1="${n1.y * h}" x2="${n2.x * w}" y2="${n2.y * h}" stroke="rgba(34,211,238,0.25)" stroke-width="1.5"/>`;
  });
  NODES.forEach((n) => {
    const sel =
      state.selectedNode === n.id
        ? ' stroke="#fbbf24" stroke-width="3"'
        : ' stroke="#22d3ee" stroke-width="1.5"';
    html += `<circle class="node-circle" data-id="${n.id}" cx="${n.x * w}" cy="${n.y * h}" r="14" fill="#1a2540"${sel} style="cursor:pointer"/>`;
    html += `<text x="${n.x * w}" y="${n.y * h + 28}" fill="#94a3b8" font-size="10" text-anchor="middle">${n.name}</text>`;
  });
  svg.innerHTML = html;
  svg.querySelectorAll(".node-circle").forEach((c) => {
    c.addEventListener("click", () => {
      state.selectedNode = c.dataset.id;
      const n = NODES.find((x) => x.id === state.selectedNode);
      const detail = document.getElementById("nodeDetail");
      if (detail) detail.textContent = JSON.stringify(n, null, 2);
      drawMesh();
      toast("Selected " + (n?.name || c.dataset.id));
      logEvent("mesh", "select " + (n?.name || c.dataset.id));
    });
  });
}

function initRoutes() {
  const ul = document.getElementById("routeList");
  if (!ul) return;
  ul.innerHTML = ROUTES.map(
    (r) =>
      `<li><span class="dest">${r.dest}</span><span class="time">${r.time} <small>(${r.status})</small></span></li>`
  ).join("");
}

function bindLayersStack() {
  document.querySelectorAll(".layer-bar").forEach((bar) => {
    bar.addEventListener("click", () => bar.classList.toggle("expanded"));
  });
}

function openWalletModal() {
  syncWalletUI();
  document.getElementById("modalWallet")?.classList.add("open");
}

function closeModals() {
  document.querySelectorAll(".modal-backdrop").forEach((m) => m.classList.remove("open"));
}

function bindEcon() {
  ["sliderBurn", "sliderAlpha", "inputBurnCore", "inputService"].forEach((id) => {
    document.getElementById(id)?.addEventListener("input", updateEconSim);
  });
  updateEconSim();
  syncWalletUI();
}

function init() {
  initNav();
  seedParticles();
  bindLayerToggles();
  renderPipeline();
  renderReceipts();
  initRoutes();
  bindLayersStack();
  bindEcon();
  drawMesh();
  animateStats();
  requestAnimationFrame(drawTwin);

  document.getElementById("btnRunPipe")?.addEventListener("click", runPipelineAuto);
  document.getElementById("btnRunPipeHome")?.addEventListener("click", runPipelineAuto);
  document.getElementById("btnBurn")?.addEventListener("click", doBurn);
  document.getElementById("btnAddReceipt")?.addEventListener("click", addReceipt);
  document.getElementById("btnWallet")?.addEventListener("click", openWalletModal);
  document.getElementById("btnWallet2")?.addEventListener("click", openWalletModal);
  document.getElementById("btnCloseModal")?.addEventListener("click", closeModals);
  document.getElementById("modalWallet")?.addEventListener("click", (e) => {
    if (e.target.id === "modalWallet") closeModals();
  });
  document.getElementById("btnClearLog")?.addEventListener("click", clearLog);
  document.getElementById("btnMeshRefresh")?.addEventListener("click", () => {
    drawMesh();
    toast("Mesh refreshed");
  });
  document.getElementById("btnGrantCap")?.addEventListener("click", () => {
    toast("Demo: capability grant issued (15m)");
    logEvent("wallet", "capability grant 15m → starline-budapest");
  });
  document.getElementById("epochSelect")?.addEventListener("change", (e) => {
    state.epoch = e.target.value;
    const pill = document.getElementById("pill-epoch");
    if (pill) pill.textContent = "epoch: " + state.epoch;
    toast("Epoch: " + state.epoch);
    logEvent("gov", "epoch " + state.epoch);
    renderPipeline();
  });

  logEvent("system", "Crystal interface ready · mainnet HOLD");
}

document.addEventListener("DOMContentLoaded", init);

window.showPanel = showPanel;
window.runPipelineAuto = runPipelineAuto;
window.doBurn = doBurn;
window.toast = toast;
window.logEvent = logEvent;
window.clearLog = clearLog;
window.confirmReceipt = confirmReceipt;
window.addReceipt = addReceipt;
