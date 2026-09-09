# CrystalVision

**Locked name** ([Constitution §1](../governance/Constitution.md)): the
sensing / dreaming / directing interface — the lens through which a human
(Crystal) watches and steers the Lattice.

## Honest status: concept with demo shells

CrystalVision is a **Vision-layer concept**. No production CrystalVision
interface exists. What does exist:

- **`src/apps/crystal-interface/`** — the operator shell: twin, mesh,
  pipeline, econ, receipts. **Simulated data, Authority HOLD.**
- **`src/apps/vision-web/`** — the citizen shell: credits, capability,
  personal twin, privacy stubs. **Simulated data, Authority HOLD.**
- **`src/site/`** — "The Crystal Vision," the public SvelteKit site. Real
  and deployed, but it is a website about the project, not a control
  surface.

"Authority HOLD" means exactly what it says: these shells render what a
control surface *would* show, and control nothing. They are not on a path to
production without a separate, reviewed decision to build the real data
layer underneath them ([`Roadmap.md`](../governance/Roadmap.md)).

## The design intent

In the design language (see [`Full-Stack-v0.5.md`](Full-Stack-v0.5.md)):
Crystal Vision faces users and citizens, Crystal Core faces operators and
builders. The interface senses (reads the twin and the mesh), dreams
(renders the mythos layer honestly, labeled), and directs (issues consented
instructions) — with the human keeping the veto at every step, per the
[Incognita Rule](../governance/The-Incognita-Rule.md) §3: no line mints its
own authority.

If and when a real CrystalVision surface is built, its first obligation is
the same one the demo shells already honour: show which of its lines are
measured and which are dreamed.
