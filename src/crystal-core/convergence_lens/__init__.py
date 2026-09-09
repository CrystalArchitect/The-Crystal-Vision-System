"""
Convergence Lens v0.1 — Interpretation Discipline

A tool for separating observation, evidence, interpretation, and vision
without replacing judgment or manufacturing certainty.

Core invariants (enforced by tests):
✓ Vision cannot impersonate evidence
✓ Interpretation cannot impersonate observation
✓ Confidence cannot replace verification
✓ Disagreement can be preserved without forced consensus
✓ Category confusion is detected and rejected

Modules:
- selftest: Verify all invariants pass
- classify: Identify statement type (observation/evidence/interpretation/vision)
- mirror: Decompose claims into components
- latency: Identify uncertainty gaps by type
- record: Create immutable Chronicle/Archive entries

Usage:
  from convergence_lens import mirror, latency_map, chronicle

  claim = "AI will create abundance within five years"

  decomposed = mirror(claim)
  gaps = latency_map(claim)
  record = chronicle(claim, decomposed, gaps)

Non-goals:
  ✗ Determine truth automatically
  ✗ Replace expert judgment
  ✗ Manufacture consensus
  ✗ Make predictions authoritative

Integration:
  - MIRROR register: decompose claims
  - LOOM register: identify patterns across claims
  - CHRONICLE register: preserve immutable records
  - CONSTITUTION: enforce invariants across all layers
"""

__version__ = '0.1.0'
__license__ = 'CC BY-NC-ND 4.0'

# Core invariant: Confidence cannot replace evidence
# This is the spine of the entire module
CENTRAL_INVARIANT = (
  "Uncertainty may be reduced by evidence. "
  "It may not be reduced by confidence."
)
