# Repository principles

The rules that keep this repository legible as it grows. They bind every
contributor, human or AI.

## At a glance

1. Documentation is not code.
2. Research is not production.
3. Preserve history — archive, don't delete.
4. Prefer incremental, reversible change.
5. Record significant architectural decisions.
6. Require review before merging.
7. Keep components loosely coupled.
8. Keep code, docs, research, and story clearly separated.
9. Favour reproducibility and clear evidence.

Nine one-liners for a quick scan; the numbered sections below are the same
nine with the reasoning and the cross-references attached.

## In full

1. **Documentation is not executable code.** `src/` holds only code;
   explanations live in `docs/`. A README may sit beside its component; a
   spec goes in `docs/architecture/`.
2. **Research is not production software.** `research/` explores freely and
   ships nothing. Promotion into `src/` is a deliberate act with review and,
   where structural, an ADR.
3. **Preserve historical material in the archive.** Superseded work moves to
   `archive/` rather than vanishing — provenance matters. Nothing there is
   maintained; never build on it.
4. **Prefer incremental, reversible change.** A conservative refactor that
   preserves behavior beats a rewrite that reaches the same place — the
   v1.0 reorganization itself moved code as a uniform shift specifically so
   nothing's runtime behavior changed underneath it
   ([`ADR-0003`](../adr/ADR-0003.md)). When a bigger step is unavoidable, cut
   it into steps that each stay revertible on their own.
5. **Record major architectural decisions.** Structural or hard-to-reverse
   choices get an ADR in [`docs/adr/`](../adr/) — see
   [`Decision-Records.md`](Decision-Records.md).
6. **Significant changes are reviewed before merging.** Branch, PR, green
   CI, maintainer merge — see [`Review-Process.md`](Review-Process.md).
7. **Keep components loosely coupled.** Clementine, the protocol pack, and
   CrystalBridge stay separate packages because they answer different trust
   questions — see ["why three, not one"](../architecture/CrystalCore.md#why-three-not-one).
   A new component earns its own boundary rather than reaching into
   another's internals.
8. **Keep code, documentation, research, and story clearly separated.** The
   mythos (`mythos/`) is Vision-layer content under its own license; it may
   point at code and never speaks for it.
9. **Favour reproducibility and clear evidence.** A claim about the software
   should come with the command that proves it (the self-tests, the test
   suites); a claim without one is labeled as vision, not fact.

Principles 8 and 9 are this repo's oldest law restated — the Belt-Three
labels ([`CONTRIBUTING.md`](../../CONTRIBUTING.md)) and the
[Incognita Rule](The-Incognita-Rule.md): mark which lines are dreamed and
which are surveyed, and never let a dreamed line pretend it was measured.

Two structural corollaries, adopted with the v1.0 architecture
([`ADR-0001`](../adr/ADR-0001.md)): the repository root stays lean (licenses,
top-level guides, and entry points only), and every directory with a
non-obvious purpose carries a README saying what belongs in it.
