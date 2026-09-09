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
  if (MAP_PANELS.includes(id)) renderMapPanel(id);
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

/* ══════════════════════════════════════════════════════════════════════
   Map suite — Lattice · Starline, Five doors, Operator flow, Ownership.

   One source: map.json. Every view below is a render of that file, so
   there is no second copy of the graph to drift out of step with it.
   Nothing here invents a status: a node shows the badge map.json gives
   it, and the sheet shows the source that badge rests on.
   ══════════════════════════════════════════════════════════════════════ */

const MAP_PANELS = ["lattice", "doors", "flow", "ownership"];

const mapState = {
  data: null,
  error: null,
  loading: null,
  selected: null,
  door: 0,
  // Filter chips. `ownership` tints rather than hides — the boundary is
  // the point of the map, not an optional decoration.
  show: { lattice: true, starline: true, horizon: true, ownership: true },
};

// Where each ring sits on the 1000×600 canvas. Angles run anticlockwise
// from east, and y is flipped so 90° reads as "up" the way a person means it.
const RING_LAYOUT = {
  core: { type: "stack", cx: 480, cy: 250, gap: 66 },
  lattice: { type: "arc", cx: 480, cy: 250, rx: 215, ry: 142, from: -20, to: 200 },
  starline: { type: "arc", cx: 480, cy: 250, rx: 400, ry: 215, from: -35, to: 215 },
  horizon: { type: "band", y: 540, x0: 220, x1: 740 },
  external: { type: "corner", x: 892, y0: 470, gap: 62 },
};

const EDGE_STYLE = {
  runtime: { stroke: "#22d3ee", dash: "", width: 1.6 },
  authoring: { stroke: "#a78bfa", dash: "7 5", width: 1.4 },
  grounding: { stroke: "#fbbf24", dash: "2 5", width: 1.4 },
  boundary_break: { stroke: "#ef4444", dash: "5 6", width: 1.4 },
};

function loadMap() {
  if (mapState.data || mapState.error) return Promise.resolve();
  if (mapState.loading) return mapState.loading;
  mapState.loading = fetch("map.json")
    .then(r => {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(d => { mapState.data = d; })
    .catch(err => { mapState.error = err.message || String(err); });
  return mapState.loading;
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function mapErrorHtml() {
  return `<div class="map-error">
    <strong>map.json could not be loaded (${esc(mapState.error)}).</strong>
    The diagram is not empty — it is unread. Opening this page straight from
    disk blocks the fetch; serve the directory instead:
    <code>python3 -m http.server</code>, then open
    <code>/interface/</code>. Published over HTTPS this path works normally.
  </div>`;
}

function renderMapPanel(id) {
  loadMap().then(() => {
    if (id === "lattice") renderLattice();
    if (id === "doors") renderDoors();
    if (id === "flow") renderFlow();
    if (id === "ownership") renderOwnership();
  });
}

// ── Layout ────────────────────────────────────────────────────────────────
function layoutNodes(nodes) {
  const pos = {};
  const byRing = {};
  nodes.forEach(n => { (byRing[n.ring] = byRing[n.ring] || []).push(n); });

  Object.keys(byRing).forEach(ring => {
    const cfg = RING_LAYOUT[ring];
    const list = byRing[ring];
    if (!cfg) return;
    if (cfg.type === "stack") {
      const top = cfg.cy - ((list.length - 1) * cfg.gap) / 2;
      list.forEach((n, i) => { pos[n.id] = { x: cfg.cx, y: top + i * cfg.gap }; });
    } else if (cfg.type === "arc") {
      const span = cfg.to - cfg.from;
      list.forEach((n, i) => {
        const t = list.length === 1 ? 0.5 : i / (list.length - 1);
        const deg = cfg.from + span * t;
        const rad = (deg * Math.PI) / 180;
        pos[n.id] = {
          x: cfg.cx + cfg.rx * Math.cos(rad),
          y: cfg.cy - cfg.ry * Math.sin(rad),
        };
      });
    } else if (cfg.type === "band") {
      const step = list.length === 1 ? 0 : (cfg.x1 - cfg.x0) / (list.length - 1);
      list.forEach((n, i) => { pos[n.id] = { x: cfg.x0 + step * i, y: cfg.y }; });
    } else if (cfg.type === "corner") {
      list.forEach((n, i) => { pos[n.id] = { x: cfg.x, y: cfg.y0 + i * cfg.gap }; });
    }
  });
  return pos;
}

// Two lines maximum, broken on a space so no word is cut in half.
function wrapLabel(label, max) {
  const words = String(label).split(" ");
  const lines = [];
  let cur = "";
  words.forEach(w => {
    if (!cur) { cur = w; return; }
    if ((cur + " " + w).length <= max) cur += " " + w;
    else { lines.push(cur); cur = w; }
  });
  if (cur) lines.push(cur);
  if (lines.length > 2) {
    return [lines[0], lines.slice(1).join(" ")];
  }
  return lines;
}

function hexPath(x, y, w, h) {
  const k = 13;
  const hw = w / 2, hh = h / 2;
  return [
    [x - hw, y],
    [x - hw + k, y - hh],
    [x + hw - k, y - hh],
    [x + hw, y],
    [x + hw - k, y + hh],
    [x - hw + k, y + hh],
  ].map(p => p.map(v => v.toFixed(1)).join(",")).join(" ");
}

function nodeVisible(n) {
  if (n.ring === "core" || n.ring === "external") return true;
  return mapState.show[n.ring] !== false;
}

// ── Lattice view ──────────────────────────────────────────────────────────
function renderLattice() {
  const svg = document.getElementById("latticeSvg");
  const stack = document.getElementById("latticeStack");
  const chips = document.getElementById("latticeFilters");
  const legend = document.getElementById("latticeLegend");
  if (!svg) return;

  if (mapState.error) {
    const wrap = svg.closest(".lattice-wrap");
    if (wrap) wrap.innerHTML = mapErrorHtml();
    if (stack) stack.innerHTML = mapErrorHtml();
    return;
  }
  const d = mapState.data;
  if (!d) return;

  renderChips(chips);
  renderLegend(legend, d);

  const W = 1000, H = 600;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const pos = layoutNodes(d.nodes);
  const byId = {};
  d.nodes.forEach(n => { byId[n.id] = n; });
  const tint = mapState.show.ownership;

  let out = "";

  // Ring guides, drawn from the same constants the nodes are placed with,
  // so what you see is the geometry rather than a decoration beside it.
  // Without these the lattice and the starlines read as one scattered field.
  [["lattice", "#22d3ee", "runtime lattice"],
   ["starline", "#a78bfa", "starlines"]].forEach(([ring, colour, label]) => {
    if (!mapState.show[ring]) return;
    const c = RING_LAYOUT[ring];
    const pts = [];
    for (let i = 0; i <= 60; i++) {
      const deg = c.from + ((c.to - c.from) * i) / 60;
      const rad = (deg * Math.PI) / 180;
      pts.push(`${(c.cx + c.rx * Math.cos(rad)).toFixed(1)},${(c.cy - c.ry * Math.sin(rad)).toFixed(1)}`);
    }
    out += `<polyline points="${pts.join(" ")}" fill="none" stroke="${colour}"
      stroke-width="1" stroke-dasharray="3 7" opacity="0.42"/>`;
    // Label sits in the gap between the last two nodes on the arc, never on
    // top of one — nodes are placed at evenly spaced angles including both ends.
    const count = d.nodes.filter(n => n.ring === ring).length;
    const step = (c.to - c.from) / Math.max(count - 1, 1);
    const r = ((c.to - step / 2) * Math.PI) / 180;
    out += `<text x="${(c.cx + c.rx * Math.cos(r)).toFixed(1)}"
      y="${(c.cy - c.ry * Math.sin(r)).toFixed(1)}" fill="${colour}" font-size="9"
      letter-spacing="1.4" text-anchor="middle" opacity="0.65">${label.toUpperCase()}</text>`;
  });

  // The dust bed the horizon stands on — Country under the tech claims.
  if (mapState.show.horizon) {
    out += `<line x1="150" y1="492" x2="810" y2="492" stroke="#7c2d12"
      stroke-width="1.5" opacity="0.7"/>`;
    out += `<text x="150" y="483" fill="#9a3412" font-size="9" letter-spacing="1.4"
      opacity="0.85">HORIZON — COUNTRY, ORDINARY LIFE</text>`;
  }

  // Boundary: everything past this arc is named, not claimed.
  out += `<path d="M 812 388 Q 872 470 838 596" fill="none" stroke="#ef4444"
    stroke-width="1" stroke-dasharray="4 7" opacity="0.55"/>`;
  out += `<text x="836" y="430" fill="#ef4444" font-size="9"
    text-anchor="middle" opacity="0.8" transform="rotate(78 836 430)">not claimed</text>`;

  // Edges first, so nodes sit above them.
  d.edges.forEach(e => {
    const a = pos[e.from], b = pos[e.to];
    const na = byId[e.from], nb = byId[e.to];
    if (!a || !b) return;
    if (!nodeVisible(na) || !nodeVisible(nb)) return;
    const st = EDGE_STYLE[e.kind] || EDGE_STYLE.runtime;
    // Trim each end so the line meets the hex rather than crossing it.
    const dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.hypot(dx, dy) || 1;
    const ux = dx / len, uy = dy / len, trim = 52;
    const x1 = a.x + ux * trim, y1 = a.y + uy * trim;
    const x2 = b.x - ux * trim, y2 = b.y - uy * trim;
    out += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}"
      x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${st.stroke}"
      stroke-width="${st.width}" stroke-dasharray="${st.dash}"
      opacity="${e.kind === "boundary_break" ? 0.8 : 0.42}"/>`;
    if (e.kind === "boundary_break") {
      const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
      out += `<g stroke="#ef4444" stroke-width="2" opacity="0.9">
        <line x1="${mx - 6}" y1="${my - 6}" x2="${mx + 6}" y2="${my + 6}"/>
        <line x1="${mx - 6}" y1="${my + 6}" x2="${mx + 6}" y2="${my - 6}"/></g>`;
    }
  });

  // Nodes.
  d.nodes.forEach(n => {
    const p = pos[n.id];
    if (!p || !nodeVisible(n)) return;
    const notYours = n.ownership === "not_yours";
    const held = n.badge === "HELD";
    const sel = mapState.selected === n.id;
    const stroke = sel ? "#fbbf24"
      : notYours ? "#334155"
      : held ? "#a78bfa"
      : n.ring === "core" ? "#fbbf24" : "#22d3ee";
    const fill = notYours ? "#0b1220" : "#1a2540";
    const op = tint && notYours ? 0.5 : 1;
    const w = n.ring === "core" ? 150 : 138, h = 42;
    const lines = wrapLabel(n.label, 17);
    const dy0 = lines.length === 1 ? 4 : -3;

    out += `<g class="lat-hit" data-id="${esc(n.id)}" tabindex="0" role="button"
      aria-label="${esc(n.label)}" opacity="${op}">`;
    out += `<polygon class="lat-shape" points="${hexPath(p.x, p.y, w, h)}"
      fill="${fill}" stroke="${stroke}" stroke-width="${sel ? 3 : 1.4}"
      stroke-linejoin="round"${held ? ' stroke-dasharray="6 4"' : ""}/>`;
    lines.forEach((ln, i) => {
      out += `<text x="${p.x.toFixed(1)}" y="${(p.y + dy0 + i * 13).toFixed(1)}"
        fill="${notYours ? "#64748b" : "#e2e8f0"}" font-size="11"
        text-anchor="middle" pointer-events="none">${esc(ln)}</text>`;
    });
    if (n.badge) {
      const bc = { LIVE: "#22d3ee", MERGED: "#22d3ee", CANON: "#fbbf24",
                   HELD: "#a78bfa", CORRECTED: "#a78bfa", EXTERNAL: "#64748b" }[n.badge];
      out += `<text x="${p.x.toFixed(1)}" y="${(p.y + h / 2 + 12).toFixed(1)}"
        fill="${bc}" font-size="8.5" letter-spacing="0.8" text-anchor="middle"
        pointer-events="none">${esc(n.badge)}</text>`;
    }
    out += `</g>`;
  });

  svg.innerHTML = out;
  svg.querySelectorAll(".lat-hit").forEach(g => {
    const open = () => openSheet(g.dataset.id);
    g.addEventListener("click", open);
    g.addEventListener("keydown", ev => {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); }
    });
  });

  renderStack(stack, d);
}

// The same JSON, arranged as rings for narrow screens.
function renderStack(el, d) {
  if (!el) return;
  let html = "";
  d.rings.forEach(r => {
    const nodes = d.nodes.filter(n => n.ring === r.id && nodeVisible(n));
    if (!nodes.length) return;
    html += `<div class="ring-group"><h4>${esc(r.label)}</h4>
      <p class="ring-blurb">${esc(r.blurb)}</p>`;
    nodes.forEach(n => {
      html += `<button class="stack-node ${esc(n.ownership)}" data-id="${esc(n.id)}">
        <span class="sn-label">${esc(n.label)}</span>
        ${n.badge ? `<span class="badge ${esc(n.badge)}">${esc(n.badge)}</span>` : ""}
      </button>`;
    });
    html += `</div>`;
  });
  el.innerHTML = html;
  el.querySelectorAll(".stack-node").forEach(b => {
    b.addEventListener("click", () => openSheet(b.dataset.id));
  });
}

function renderChips(el) {
  if (!el) return;
  const defs = [
    ["lattice", "Runtime"],
    ["starline", "Starlines"],
    ["horizon", "Horizon"],
    ["ownership", "Ownership tint"],
  ];
  el.innerHTML = defs.map(([k, label]) =>
    `<button class="toggle ${mapState.show[k] ? "on" : ""}" data-flag="${k}">${label}</button>`
  ).join("");
  el.querySelectorAll("[data-flag]").forEach(b => {
    b.addEventListener("click", () => {
      const k = b.dataset.flag;
      mapState.show[k] = !mapState.show[k];
      renderLattice();
    });
  });
}

function renderLegend(el, d) {
  if (!el) return;
  const edges = [
    ["runtime", "Runtime dependency or consent path"],
    ["authoring", "Authoring — mythos and logos"],
    ["grounding", "Grounds — what the code must match"],
    ["boundary_break", "Ownership boundary — no claim crosses it"],
  ];
  let html = edges.map(([k, t]) =>
    `<div class="legend-row"><span class="legend-swatch ${k}"></span><span>${esc(t)}</span></div>`
  ).join("");
  html += Object.keys(d.badges).map(b =>
    `<div class="legend-row"><span class="badge ${esc(b)}">${esc(b)}</span>
     <span>${esc(d.badges[b])}</span></div>`
  ).join("");
  el.innerHTML = html;
}

// ── Node sheet ────────────────────────────────────────────────────────────
function openSheet(id) {
  const d = mapState.data;
  if (!d) return;
  const n = d.nodes.find(x => x.id === id);
  if (!n) return;
  mapState.selected = id;

  const ring = d.rings.find(r => r.id === n.ring);
  const related = d.edges.filter(e => e.from === id || e.to === id);
  const nameOf = x => (d.nodes.find(y => y.id === x) || { label: x }).label;
  const ownWord = { yours: "Yours", not_yours: "Not yours",
                    shared_context: "Shared context" }[n.ownership] || n.ownership;

  document.getElementById("sheetTitle").textContent = n.label;
  document.getElementById("sheetBody").innerHTML = `
    <div class="sheet-meta">
      ${n.badge ? `<span class="badge ${esc(n.badge)}">${esc(n.badge)}</span>` : ""}
      <span class="own-tint ${esc(n.ownership)}">${esc(ownWord)}</span>
      <span class="own-tint">${esc(ring ? ring.label : n.ring)}</span>
    </div>
    <p>${esc(n.blurb)}</p>
    <h4>Source</h4>
    <div class="src">${esc(n.source || "—")}</div>
    <h4>Edges</h4>
    <ul>${related.map(e => `<li>${e.from === id
        ? `${esc(e.label)} → ${esc(nameOf(e.to))}`
        : `${esc(nameOf(e.from))} — ${esc(e.label)} → this`}</li>`).join("") ||
      "<li>none recorded</li>"}</ul>`;

  document.getElementById("nodeSheet").classList.add("open");
  logEvent("map", "node " + n.id);
  if (document.getElementById("panel-lattice").classList.contains("active")) renderLattice();
}

function closeSheet() {
  document.getElementById("nodeSheet").classList.remove("open");
  mapState.selected = null;
  if (document.getElementById("panel-lattice").classList.contains("active")) renderLattice();
}

// ── Five doors ────────────────────────────────────────────────────────────
function renderDoors() {
  const row = document.getElementById("doorRow");
  const detail = document.getElementById("doorDetail");
  const note = document.getElementById("doorsNote");
  if (!row) return;
  if (mapState.error) { row.innerHTML = mapErrorHtml(); return; }
  const d = mapState.data;
  if (!d) return;

  row.innerHTML = d.doors.map((dr, i) =>
    `<button class="door-step ${i === mapState.door ? "active" : ""}" data-i="${i}">
      <span class="dn">Door ${dr.n}</span><span class="dl">${esc(dr.label)}</span>
    </button>`).join("");
  row.querySelectorAll(".door-step").forEach(b => {
    b.addEventListener("click", () => {
      mapState.door = parseInt(b.dataset.i, 10);
      renderDoors();
    });
  });

  const cur = d.doors[mapState.door];
  detail.innerHTML = `<p class="asks">${esc(cur.asks)}</p>
    <p class="muted">${esc(cur.detail)}</p>
    <p class="refuses">refuses: ${esc(cur.refuses)}</p>`;
  if (note) note.textContent = d.doors_note;
}

// ── Operator flow ─────────────────────────────────────────────────────────
function renderFlow() {
  const row = document.getElementById("flowRow");
  if (!row) return;
  if (mapState.error) { row.innerHTML = mapErrorHtml(); return; }
  const d = mapState.data;
  if (!d) return;

  row.innerHTML = d.flow.map(s => `
    <div class="flow-step ${esc(s.status)}">
      <span class="status">${s.status === "real" ? "runs today" : "designed, not built"}</span>
      <h4>${s.n}. ${esc(s.label)}</h4>
      <p>${esc(s.detail)}</p>
      ${s.commands ? `<pre>${s.commands.map(esc).join("\n")}</pre>` : ""}
      <p class="src" style="font-size:0.68rem">${esc(s.source)}</p>
    </div>`).join("");
}

// ── Ownership boundary ────────────────────────────────────────────────────
function renderOwnership() {
  const cols = document.getElementById("ownCols");
  const note = document.getElementById("ownNote");
  if (!cols) return;
  if (mapState.error) { cols.innerHTML = mapErrorHtml(); return; }
  const d = mapState.data;
  if (!d) return;

  const yours = d.nodes.filter(n => n.ownership === "yours");
  const theirs = d.nodes.filter(n => n.ownership === "not_yours");
  const shared = d.nodes.filter(n => n.ownership === "shared_context");
  // Operating a node is not the same as having built it. A node carries its
  // badge into this column too, so "yours" never quietly reads as "exists".
  const chip = n => `<span class="own-item">${esc(n.label)}${
    n.badge ? ` <span class="badge ${esc(n.badge)}">${esc(n.badge)}</span>` : ""}</span>`;

  cols.innerHTML = `
    <div class="own-col yours">
      <h4>Claimed — used in these systems</h4>
      <div class="own-list">${d.claimed.map(m =>
        `<span class="own-item">${esc(m)}</span>`).join("")}</div>
      <h4 style="margin-top:0.9rem">Nodes you operate</h4>
      <div class="own-list">${yours.map(chip).join("")}</div>
      <p class="muted small" style="margin:0.7rem 0 0">${esc(d.ownership_note)}</p>
    </div>
    <div class="own-col not_yours">
      <h4>Named, not claimed</h4>
      <div class="own-list">${d.not_claimed.map(m =>
        `<span class="own-item">${esc(m)}</span>`).join("")}</div>
      <h4 style="margin-top:0.9rem">Outside the boundary</h4>
      <div class="own-list">${theirs.map(chip).join("")}</div>
      <p class="muted small" style="margin:0.7rem 0 0">${esc(d.not_claimed_note)}</p>
    </div>
    ${shared.length ? `<div class="own-col shared">
      <h4>Neither column — shared context</h4>
      <div class="own-list">${shared.map(chip).join("")}</div>
      <p class="muted small" style="margin:0.7rem 0 0">Country is not property.
      It grounds the work and is not claimed by it, so it sits in neither
      column rather than being filed under one for tidiness.</p>
    </div>` : ""}`;
  if (note) note.textContent = d._about.caption;
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

  // Node sheet: button, backdrop click, and Escape all dismiss it. A sheet
  // you cannot close is a trap, not a detail pane.
  document.getElementById("btnCloseSheet")?.addEventListener("click", closeSheet);
  document.getElementById("nodeSheet")?.addEventListener("click", ev => {
    if (ev.target.id === "nodeSheet") closeSheet();
  });
  document.addEventListener("keydown", ev => {
    if (ev.key === "Escape" &&
        document.getElementById("nodeSheet")?.classList.contains("open")) closeSheet();
  });
  document.getElementById("epochSelect")?.addEventListener("change", e => {
    state.epoch = e.target.value;
    toast("Epoch: " + state.epoch);
  });

  window.confirmReceipt = confirmReceipt;
});
