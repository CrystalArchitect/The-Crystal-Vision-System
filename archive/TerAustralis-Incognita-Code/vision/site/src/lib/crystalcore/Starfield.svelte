<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  let { flying = false } = $props();

  let canvasEl = $state(null);

  // Plain (non-reactive) handoff between the mount effect, which owns the
  // draw loop, and the flying-prop effect, which only needs to nudge the
  // warp target — mutating these must not re-trigger the mount effect.
  let warpTarget = 0;
  let reduced = false;
  let redraw = null;

  $effect(() => {
    warpTarget = flying ? 1 : 0;
    if (reduced) redraw?.();
  });

  $effect(() => {
    if (!canvasEl) return;
    reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const cv = canvasEl;
    const cx = cv.getContext('2d');
    let w, h, stars = [], shoot = null, warp = 0, raf = null;

    function size() {
      w = cv.width = window.innerWidth * devicePixelRatio;
      h = cv.height = window.innerHeight * devicePixelRatio;
      cv.style.width = window.innerWidth + 'px';
      cv.style.height = window.innerHeight + 'px';
      seed();
    }

    function seed() {
      stars = [];
      const n = Math.round((w * h) / (14000 * devicePixelRatio));
      for (let i = 0; i < n; i++) {
        stars.push({
          x: (Math.random() - 0.5) * w * 2,
          y: (Math.random() - 0.5) * h * 2,
          z: Math.random() * w,
          hue: 196 + Math.random() * 104, // locked to the arc
          m: 0.35 + Math.random() * 0.65
        });
      }
    }

    function draw() {
      warp += (warpTarget - warp) * 0.045;

      cx.fillStyle = '#06070E';
      cx.fillRect(0, 0, w, h);

      const cxp = w / 2, cyp = h / 2;

      // nebula, violet, very low
      const g = cx.createRadialGradient(cxp * 1.15, cyp * 0.7, 0, cxp * 1.15, cyp * 0.7, w * 0.62);
      g.addColorStop(0, 'rgba(102,65,219,.13)');
      g.addColorStop(0.55, 'rgba(60,220,229,.035)');
      g.addColorStop(1, 'rgba(6,7,14,0)');
      cx.fillStyle = g;
      cx.fillRect(0, 0, w, h);

      for (let i = 0; i < stars.length; i++) {
        const s = stars[i];
        s.z -= (0.35 + warp * 26) * devicePixelRatio;
        if (s.z < 1) {
          s.z = w;
          s.x = (Math.random() - 0.5) * w * 2;
          s.y = (Math.random() - 0.5) * h * 2;
        }

        const k = 128 / s.z;
        const px = cxp + s.x * k, py = cyp + s.y * k;
        if (px < 0 || px > w || py < 0 || py > h) continue;

        const r = Math.max(0.4, (1 - s.z / w) * 2.1 * s.m) * devicePixelRatio;
        const a = (1 - s.z / w) * s.m;

        if (warp > 0.05) {
          const pz = s.z + (0.35 + warp * 26) * devicePixelRatio * 7;
          const k2 = 128 / pz;
          cx.strokeStyle = 'hsla(' + s.hue + ',72%,66%,' + a * 0.8 + ')';
          cx.lineWidth = r;
          cx.beginPath();
          cx.moveTo(cxp + s.x * k2, cyp + s.y * k2);
          cx.lineTo(px, py);
          cx.stroke();
        } else {
          cx.fillStyle = 'hsla(' + s.hue + ',70%,68%,' + a + ')';
          cx.beginPath();
          cx.arc(px, py, r, 0, 6.283);
          cx.fill();
        }
      }

      // rare violet-tailed shooting star
      if (!shoot && warp < 0.1 && Math.random() < 0.0016) {
        shoot = { x: Math.random() * w, y: Math.random() * h * 0.5, vx: -5.5 * devicePixelRatio, vy: 2.6 * devicePixelRatio, life: 1 };
      }
      if (shoot) {
        const sg = cx.createLinearGradient(shoot.x, shoot.y, shoot.x - shoot.vx * 17, shoot.y - shoot.vy * 17);
        sg.addColorStop(0, 'rgba(201,121,236,' + shoot.life * 0.9 + ')');
        sg.addColorStop(1, 'rgba(132,67,232,0)');
        cx.strokeStyle = sg;
        cx.lineWidth = 1.7 * devicePixelRatio;
        cx.beginPath();
        cx.moveTo(shoot.x, shoot.y);
        cx.lineTo(shoot.x - shoot.vx * 17, shoot.y - shoot.vy * 17);
        cx.stroke();
        shoot.x += shoot.vx;
        shoot.y += shoot.vy;
        shoot.life -= 0.014;
        if (shoot.life <= 0) shoot = null;
      }

      if (!reduced) raf = requestAnimationFrame(draw);
    }

    redraw = draw;
    window.addEventListener('resize', size);
    size();
    draw();

    return () => {
      window.removeEventListener('resize', size);
      if (raf) cancelAnimationFrame(raf);
      redraw = null;
    };
  });
</script>

<canvas bind:this={canvasEl}></canvas>

<style>
  canvas {
    position: fixed;
    inset: 0;
    z-index: 0;
    display: block;
  }
</style>
