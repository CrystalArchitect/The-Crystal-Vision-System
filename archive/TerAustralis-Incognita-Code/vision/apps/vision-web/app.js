// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

/* Crystal Vision — citizen shell (demo, not production) */
const state = {
  credits: 1240.5,
  receipts: [],
  capability: null,
  layers: { water: true, energy: true, mobility: true },
};

function toast(msg) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2600);
}

function showPanel(id) {
  document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
  const panel = document.getElementById("panel-" + id);
  if (panel) panel.classList.add("active");
  document.querySelector(`.nav-btn[data-panel="${id}"]`)?.classList.add("active");
  if (id === "twin") drawTwin();
  if (id === "receipts") renderReceipts();
}

function syncCredits() {
  const el = document.getElementById("statCredits");
  if (el) el.textContent = Math.round(state.credits).toLocaleString();
}

function drawTwin() {
  const c = document.getElementById("twinCanvas");
  if (!c) return;
  const ctx = c.getContext("2d");
  const w = c.width;
  const h = c.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#000000";
  ctx.fillRect(0, 0, w, h);

  // Danube-ish curve
  if (state.layers.water) {
    ctx.strokeStyle = "rgba(122, 162, 255, 0.55)";
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.moveTo(0, h * 0.55);
    for (let x = 0; x <= w; x += 20) {
      ctx.lineTo(x, h * 0.55 + Math.sin(x / 80) * 28 + Math.cos(x / 40) * 8);
    }
    ctx.stroke();
  }

  // Energy nodes
  if (state.layers.energy) {
    const nodes = [
      [0.2, 0.35],
      [0.45, 0.4],
      [0.7, 0.32],
      [0.55, 0.65],
    ];
    ctx.fillStyle = "rgba(167, 139, 250, 0.85)";
    nodes.forEach(([nx, ny], i) => {
      const x = nx * w;
      const y = ny * h;
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      if (i > 0) {
        const [px, py] = nodes[i - 1];
        ctx.strokeStyle = "rgba(167, 139, 250, 0.25)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(px * w, py * h);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
    });
  }

  // Mobility corridors
  if (state.layers.mobility) {
    ctx.strokeStyle = "rgba(233, 187, 95, 0.5)";
    ctx.lineWidth = 3;
    ctx.setLineDash([8, 6]);
    ctx.beginPath();
    ctx.moveTo(w * 0.05, h * 0.25);
    ctx.lineTo(w * 0.4, h * 0.3);
    ctx.lineTo(w * 0.75, h * 0.22);
    ctx.lineTo(w * 0.95, h * 0.35);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  ctx.fillStyle = "#A6ACC4";
  ctx.font = "12px system-ui";
  ctx.fillText("Starline Budapest · personal slice (demo)", 16, 24);
}

function capExpired() {
  return !state.capability || Date.now() > state.capability.until;
}

function renderCap() {
  const el = document.getElementById("capState");
  if (!el) return;
  if (capExpired()) {
    state.capability = null;
    el.textContent = "capability: none";
    return;
  }
  const left = Math.max(0, Math.round((state.capability.until - Date.now()) / 1000));
  el.textContent = JSON.stringify(
    {
      id: state.capability.id,
      scope: state.capability.scope,
      expires_in_s: left,
      region: "budapest-starline",
    },
    null,
    2
  );
}

function grantCap() {
  state.capability = {
    id: "cap-" + Date.now().toString(36),
    scope: ["mobility.ride", "energy.kwh", "water.m3", "data.mb"],
    until: Date.now() + 15 * 60 * 1000,
  };
  renderCap();
  document.getElementById("statCap").textContent = "15m";
  toast("Capability granted (15 minutes, demo)");
}

function spend() {
  if (capExpired()) {
    toast("Need an active capability first");
    return;
  }
  const cls = document.getElementById("svcClass")?.value || "mobility.ride";
  const qty = parseFloat(document.getElementById("svcQty")?.value || "1");
  const cost = parseFloat(document.getElementById("svcCost")?.value || "12.5");
  if (cost > state.credits) {
    toast("Insufficient credits (demo)");
    return;
  }
  if (!state.capability.scope.includes(cls)) {
    toast("Class out of capability scope");
    return;
  }
  state.credits = Math.max(0, state.credits - cost);
  syncCredits();
  const r = {
    id: "vrx-" + Date.now().toString(36),
    class: cls,
    qty,
    credits: cost,
    status: "confirmed",
  };
  state.receipts.unshift(r);
  renderReceipts();
  toast("Receipt " + r.id + " · confirmed (demo, not attested)");
  renderCap();
}

function renderReceipts() {
  const tbody = document.getElementById("rxBody");
  if (!tbody) return;
  tbody.innerHTML =
    state.receipts
      .slice(0, 20)
      .map(
        (r) =>
          `<tr><td class="mono">${r.id}</td><td>${r.class}</td><td>${r.qty}</td><td>${r.credits}</td><td>${r.status}</td></tr>`
      )
      .join("") || "<tr><td colspan='5'>No receipts yet</td></tr>";
}

function exportData() {
  const payload = {
    schema: "crystal.vision.export/1",
    region: "budapest-starline",
    credits: state.credits,
    receipts: state.receipts,
    note: "Demo export — not a legal GDPR package",
  };
  const el = document.getElementById("privacyOut");
  if (el) el.textContent = JSON.stringify(payload, null, 2);
  toast("Export rendered (client-side only)");
}

function requestErase() {
  state.receipts = [];
  state.capability = null;
  renderReceipts();
  renderCap();
  const el = document.getElementById("privacyOut");
  if (el) {
    el.textContent = JSON.stringify(
      {
        request: "erase_personal_slice",
        status: "queued_demo",
        authority: "HOLD",
        note: "No live controller — see compliance/GDPR_ROPA.md",
      },
      null,
      2
    );
  }
  toast("Erase request logged (demo)");
}

function init() {
  document.querySelectorAll(".nav-btn").forEach((b) => {
    b.addEventListener("click", () => showPanel(b.dataset.panel));
  });
  document.querySelectorAll("[data-go]").forEach((b) => {
    b.addEventListener("click", () => showPanel(b.dataset.go));
  });
  document.querySelectorAll("[data-layer]").forEach((inp) => {
    inp.addEventListener("change", () => {
      state.layers[inp.dataset.layer] = inp.checked;
      drawTwin();
    });
  });
  document.getElementById("btnGrant")?.addEventListener("click", grantCap);
  document.getElementById("btnSpend")?.addEventListener("click", spend);
  document.getElementById("btnRefreshRx")?.addEventListener("click", renderReceipts);
  document.getElementById("btnExport")?.addEventListener("click", exportData);
  document.getElementById("btnErase")?.addEventListener("click", requestErase);
  document.getElementById("btnWallet")?.addEventListener("click", () => {
    toast("Credits: " + state.credits.toFixed(2) + " (demo)");
  });
  syncCredits();
  drawTwin();
  setInterval(renderCap, 1000);
}

document.addEventListener("DOMContentLoaded", init);
