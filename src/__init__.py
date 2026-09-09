"""CrystalCore — sovereign edge AGI framework.

Modules:
    crystal_memory  — sparse, quantized, consent-aware memory substrate
    crystal_flow    — autograd + inspectable symbolic reasoning over memory
    crystal_evolve  — population-based training of hybrid genomes
    crystal_mind    — four named reasoning-policy agents (non-autonomous)
    crystal_sensor  — external input abstraction (text/audio/env/device); external world only
    crystal_lattice — relational substrate: consent-gated handoffs between nodes/devices/LLMs
    policy_rules    — substantive rules for a policy-drafting use case
"""

from .crystal_memory import (
    CrystalMemory, SparseTensor, CoherenceMetadata,
    HierarchicalNode, ConsumerRegistry,
)
from .crystal_flow import (
    Value, sgd_step, zero_grad,
    CrystalFlow, Rule, Fact, ConsentViolation, StepRecord,
)
from .crystal_evolve import (
    CrystalEvolve, RuleRegistry, Genome, FitnessResult,
)
from .crystal_mind import (
    CrystalMind, AgentSpec, AgentResult,
)
from .crystal_sensor import (
    SensorType, SensorReading, SensorInputHandler, MockSensors,
)
from .crystal_lattice import (
    CrystalLattice, LatticeNode, HandoffEnvelope, detect_platform,
)
from . import policy_rules

__version__ = "0.6.0"
