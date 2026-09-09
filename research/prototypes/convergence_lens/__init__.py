"""
Convergence Lens Prototype

An interpretation discipline for emerging ideas, claims, and signals.
Improves recognition without replacing judgment.

Core modules:
- classifier: Decompose statements into observation/evidence/interpretation/vision
- uncertainty_mapper: Identify gaps (knowledge/tech/resource/coordination/trust)
- evidence_status: Track confidence and evidence tier over time
- transcript: Preserve dialogue exchanges for later review

Architecture:
ARCHIVE (memory) ← MIRROR (decomposition) ← LOOM (patterns)
                ← CHRONICLE (evolution) ← CONSTITUTION (rules)
                ← FORGE (scenario testing)

Non-autonomous: This prototype does not make predictions, create consensus,
replace experts, or output conclusions. It decomposes, records, and reflects.

Central invariant: Uncertainty may be reduced by evidence. It may not be
reduced by confidence.
"""

from .classifier import Classification, classify
from .uncertainty_mapper import Uncertainty, UncertaintyMap, map_uncertainty
from .evidence_status import EvidenceStatus, StatusTimeline
from .transcript import Turn, Transcript

__version__ = '0.1.0'
__all__ = [
  'Classification',
  'classify',
  'Uncertainty',
  'UncertaintyMap',
  'map_uncertainty',
  'EvidenceStatus',
  'StatusTimeline',
  'Turn',
  'Transcript',
]
