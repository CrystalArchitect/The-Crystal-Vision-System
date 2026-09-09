#!/usr/bin/env python3
"""
CrystalMemory - Sovereign Edge Memory Substrate for CrystalCore
Part of the CrystalCore Sovereign Edge AGI Framework

Production-grade, edge-first memory substrate. Designed for constrained
hardware (Raspberry Pi 4/5, low-power embedded devices) in offline or
low-connectivity environments.

Hardening (v2):
- Atomic, corruption-resistant persistence (.tmp + os.replace + SHA-256 checksum)
- Real RAM profiling via recursive sys.getsizeof traversal
- Graceful degradation: symbolic fallback (hash-only) under memory pressure
- First-class consent: ConsumerRegistry with bitmask permissions + access log
- Optional temporal decay with tunable half-life
- Weighted eviction: coherence * family_priority * temporal_weight
- Hierarchical summarization (non-destructive by default; explicit collapse)

Dependencies: standard library only. NumPy optional. No cryptography beyond
hashlib (standard library, used for integrity checksums and IDs only).
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import time
import os
import sys
import math

try:
    import numpy as np
except ImportError:
    np = None


# --------------------------------------------------------------------------- #
# Metadata
# --------------------------------------------------------------------------- #
@dataclass
class CoherenceMetadata:
    """Truth, provenance, consent and family weighting metadata."""
    coherence_score: float = 0.0
    provenance_hash: str = ""
    consent_flags: int = 0          # Bitmask: bit 0 = user, bit 1 = family, etc.
    temporal_weight: float = 1.0
    family_priority: float = 1.0
    timestamp: float = field(default_factory=time.time)
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoherenceMetadata":
        # Tolerate unknown/legacy keys so old files still load.
        allowed = cls.__dataclass_fields__.keys()
        clean = {k: v for k, v in data.items() if k in allowed}
        return cls(**clean)


# --------------------------------------------------------------------------- #
# Sparse tensor
# --------------------------------------------------------------------------- #
@dataclass
class SparseTensor:
    """Lightweight sparse tensor (COO format + quantization)."""
    shape: Tuple[int, ...]
    indices: List[Tuple[int, ...]]
    values: List[float]
    scale: float = 1.0
    zero_point: int = 0
    quantized: bool = False
    metadata: CoherenceMetadata = field(default_factory=CoherenceMetadata)

    def __post_init__(self):
        self._recompute_sparsity()

    def _recompute_sparsity(self):
        total = math.prod(self.shape) if self.shape else 1
        self.sparsity = len(self.indices) / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "shape": list(self.shape),
            "indices": [list(i) for i in self.indices],
            "values": self.values,
            "scale": self.scale,
            "zero_point": self.zero_point,
            "quantized": self.quantized,
            "metadata": self.metadata.to_dict(),
        }
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SparseTensor":
        meta = CoherenceMetadata.from_dict(data.get("metadata", {}))
        return cls(
            shape=tuple(data.get("shape", ())),
            indices=[tuple(i) for i in data.get("indices", [])],
            values=list(data.get("values", [])),
            scale=data.get("scale", 1.0),
            zero_point=data.get("zero_point", 0),
            quantized=data.get("quantized", False),
            metadata=meta,
        )

    def quantize(self, bit_width: int = 8) -> None:
        """Quantize values in-place to an unsigned integer range."""
        if not self.values:
            self.quantized = True
            return
        max_v, min_v = max(self.values), min(self.values)
        if max_v == min_v:
            self.scale, self.zero_point = 1.0, 0
            self.values = [0] * len(self.values)
            self.quantized = True
            self._recompute_sparsity()
            return
        levels = (1 << bit_width) - 1
        self.scale = (max_v - min_v) / levels
        self.zero_point = round(-min_v / self.scale)
        self.values = [
            max(0, min(levels, round((v / self.scale) + self.zero_point)))
            for v in self.values
        ]
        self.quantized = True
        self._recompute_sparsity()

    def dequantize(self) -> List[float]:
        """Return approximate original float values (non-destructive)."""
        if not self.quantized:
            return list(self.values)
        return [(v - self.zero_point) * self.scale for v in self.values]


# --------------------------------------------------------------------------- #
# Hierarchical node
# --------------------------------------------------------------------------- #
@dataclass
class HierarchicalNode:
    """Hierarchical node for compression and long-context recall."""
    id: str
    content: Any
    children: List[str] = field(default_factory=list)
    summary: Optional[Dict[str, Any]] = None
    metadata: CoherenceMetadata = field(default_factory=CoherenceMetadata)
    # Durable payload for non-numeric conclusions: policy text, family
    # decisions, creative fragments, Evolve genomes. Survives round-trips
    # independently of the (numeric) tensor in `content`. None for pure
    # numeric nodes and for nodes loaded from pre-payload files.
    payload: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "children": list(self.children),
            "summary": self.summary,
            "metadata": self.metadata.to_dict(),
            "payload": self.payload,
        }
        if isinstance(self.content, SparseTensor):
            d["content"] = self.content.to_dict()
        else:
            d["content"] = self.content
        return d


# --------------------------------------------------------------------------- #
# Consumer registry (consent + audit)
# --------------------------------------------------------------------------- #
@dataclass
class ConsumerRegistry:
    """
    Minimal consent enforcement and audit trail.

    consumers: {consumer_id: {"name": str, "permissions": int, "registered_at": float}}
        'permissions' is a bitmask that is ANDed against a node's consent_flags.
    access_log: append-only list of access events for auditability.
    """
    consumers: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    access_log: List[Dict[str, Any]] = field(default_factory=list)
    max_log_entries: int = 5000  # Bounded for edge RAM safety.

    def register(self, consumer_id: str, name: str, permissions: int = 0b1) -> None:
        self.consumers[consumer_id] = {
            "name": name,
            "permissions": permissions,
            "registered_at": time.time(),
        }

    def revoke(self, consumer_id: str) -> bool:
        """Revoke a consumer's access without deleting data."""
        if consumer_id in self.consumers:
            self.consumers[consumer_id]["permissions"] = 0
            self._log(consumer_id, "<registry>", "revoked")
            return True
        return False

    def is_allowed(self, consumer_id: str, consent_flags: int) -> bool:
        if consumer_id not in self.consumers:
            return False
        return bool(self.consumers[consumer_id]["permissions"] & consent_flags)

    def _log(self, consumer_id: str, node_id: str, action: str) -> None:
        self.access_log.append({
            "consumer_id": consumer_id,
            "node_id": node_id,
            "action": action,
            "timestamp": time.time(),
        })
        # Bound the log so it never blows the RAM budget on long-running devices.
        if len(self.access_log) > self.max_log_entries:
            self.access_log = self.access_log[-self.max_log_entries:]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "consumers": self.consumers,
            "access_log": self.access_log,
            "max_log_entries": self.max_log_entries,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsumerRegistry":
        reg = cls(
            consumers=data.get("consumers", {}),
            access_log=data.get("access_log", []),
            max_log_entries=data.get("max_log_entries", 5000),
        )
        return reg


# --------------------------------------------------------------------------- #
# Main memory substrate
# --------------------------------------------------------------------------- #
class CrystalMemory:
    """
    Sovereign edge memory substrate.
    Hierarchical, sparse, coherence-first storage with built-in consent,
    provenance, atomic persistence, and graceful degradation.
    """

    DEFAULT_CONSUMER = "default"

    def __init__(
        self,
        max_ram_mb: float = 256,
        storage_path: str = "crystal_memory.json",
        decay_half_life_days: float = 45.0,
        default_temporal_decay: bool = False,
    ):
        self.max_ram_mb = max_ram_mb
        self.storage_path = storage_path
        self.decay_half_life_days = decay_half_life_days
        self.default_temporal_decay = default_temporal_decay

        self.nodes: Dict[str, HierarchicalNode] = {}
        self.registry = ConsumerRegistry()
        self.root_id = "root"
        self.coherence_threshold = 0.6
        self._current_size_estimate = 0
        self.last_status = "ok"  # Surfaces recovery / degradation state.

        if self.root_id not in self.nodes:
            self.nodes[self.root_id] = HierarchicalNode(id=self.root_id, content={})

        # A default consumer that can see user-flagged (bit 0) data.
        self.registry.register(self.DEFAULT_CONSUMER, "Default User", permissions=0b1)

        self._load_from_disk()

    # --- ID generation ------------------------------------------------------ #
    def _generate_id(self, data: Any) -> str:
        h = hashlib.sha256()
        h.update(str(data).encode("utf-8"))
        h.update(str(time.time()).encode("utf-8"))
        return h.hexdigest()[:16]

    def _data_hash(self, data: Any) -> str:
        return hashlib.sha256(str(data).encode("utf-8")).hexdigest()

    # --- Consumer management ------------------------------------------------ #
    def register_consumer(self, consumer_id: str, name: str, permissions: int = 0b1) -> None:
        self.registry.register(consumer_id, name, permissions)

    def revoke_consumer(self, consumer_id: str) -> bool:
        return self.registry.revoke(consumer_id)

    # --- Encoding ----------------------------------------------------------- #
    def encode(
        self,
        data: Any,
        coherence_boost: float = 1.0,
        consent_flags: int = 1,
        family_priority: float = 1.0,
        bit_width: int = 8,
        payload: Optional[Any] = None,
    ) -> str:
        """Encode data into memory with coherence and consent metadata.

        `payload` (optional) stores durable non-numeric content (str/dict) that
        survives round-trips independently of the numeric tensor. Use it for
        policy text, family decisions, creative fragments, or genomes.

        Falls back to a symbolic (hash-only) node under MemoryError so the
        system stays usable under extreme pressure.
        """
        node_id = self._generate_id(data)
        metadata = CoherenceMetadata(
            coherence_score=min(1.0, coherence_boost * 0.8),
            provenance_hash=self._payload_aware_hash(data, payload),
            consent_flags=consent_flags,
            family_priority=family_priority,
        )

        try:
            content = self._build_tensor(data, bit_width)
            node = HierarchicalNode(
                id=node_id, content=content, metadata=metadata, payload=payload
            )
        except MemoryError:
            # Graceful degradation -> symbolic node (payload still preserved
            # if it fits; it is small text/dict, not the bulky tensor).
            node = self._build_symbolic_node(node_id, data, metadata)
            node.payload = payload
            self.last_status = "degraded_symbolic"

        self.nodes[self.root_id].children.append(node_id)
        self.nodes[node_id] = node

        self._estimate_size()
        self._prune_if_needed()
        self.save_to_disk()
        return node_id

    def _payload_aware_hash(self, data: Any, payload: Optional[Any]) -> str:
        """Provenance hash over both the numeric data and the durable payload,
        so verification covers whichever the node actually carries."""
        h = hashlib.sha256()
        h.update(str(data).encode("utf-8"))
        if payload is not None:
            h.update(b"|payload|")
            h.update(json.dumps(payload, sort_keys=True,
                                ensure_ascii=False).encode("utf-8"))
        return h.hexdigest()

    def _build_tensor(self, data: Any, bit_width: int) -> SparseTensor:
        if isinstance(data, (list, tuple)) or (np and isinstance(data, np.ndarray)):
            arr = (
                data.flatten().tolist()
                if (np and isinstance(data, np.ndarray))
                else list(data)
            )
            indices = [(i,) for i, v in enumerate(arr) if abs(v) > 1e-6]
            values = [float(v) for v in arr if abs(v) > 1e-6]
            tensor = SparseTensor(shape=(len(arr),), indices=indices, values=values)
            tensor.quantize(bit_width)
            return tensor
        # Scalars / unsupported types -> minimal tensor placeholder.
        return SparseTensor(shape=(1,), indices=[(0,)], values=[0.0])

    def _build_symbolic_node(
        self, node_id: str, data: Any, metadata: CoherenceMetadata
    ) -> HierarchicalNode:
        """Hash-only fallback node. Verifiable, tiny, non-reconstructable."""
        metadata.coherence_score = min(metadata.coherence_score, 0.3)
        return HierarchicalNode(
            id=node_id,
            content={"type": "symbolic", "hash": self._data_hash(data)},
            metadata=metadata,
        )

    # --- Retrieval ---------------------------------------------------------- #
    def _effective_coherence(self, node: HierarchicalNode, apply_decay: bool) -> float:
        base = node.metadata.coherence_score
        if not apply_decay:
            return base
        age_days = (time.time() - node.metadata.timestamp) / 86400.0
        if self.decay_half_life_days <= 0:
            return base
        decay_factor = 0.5 ** (age_days / self.decay_half_life_days)
        return base * decay_factor

    def encode_derived(
        self,
        data: Any,
        parent_ids: List[str],
        coherence: float,
        consent_flags: int = 1,
        family_priority: float = 1.0,
        rule: str = "",
        bit_width: int = 8,
        payload: Optional[Any] = None,
    ) -> str:
        """Encode a *derived* node whose provenance links to parent nodes.

        Used by reasoning layers (e.g. CrystalFlow) to write conclusions back
        into memory with an explicit, auditable derivation trail. The caller is
        responsible for having already computed `coherence` (e.g. via a
        conservative propagation rule) and for consent enforcement on the
        inputs. We still record the parent links and rule for inspectability.

        `data` should be numeric (list/tuple) for the tensor. For non-numeric
        conclusions (policy text, decisions, genomes), pass the real content as
        `payload` and a lightweight numeric placeholder as `data`.
        """
        # Allow callers to pass non-numeric data directly: route it to payload
        # and keep a tiny numeric placeholder so the tensor path stays valid.
        if payload is None and not isinstance(data, (list, tuple)) and not (
            np and isinstance(data, np.ndarray)
        ):
            payload = data
            data = [0.0]

        node_id = self._generate_id(data if payload is None else payload)
        metadata = CoherenceMetadata(
            coherence_score=max(0.0, min(1.0, coherence)),
            provenance_hash=self._payload_aware_hash(data, payload),
            consent_flags=consent_flags,
            family_priority=family_priority,
        )
        try:
            content = self._build_tensor(data, bit_width)
            node = HierarchicalNode(
                id=node_id, content=content, metadata=metadata, payload=payload
            )
        except MemoryError:
            node = self._build_symbolic_node(node_id, data, metadata)
            node.payload = payload
            self.last_status = "degraded_symbolic"

        # Record derivation in the node summary (cheap, inspectable).
        node.summary = {
            "derived": True,
            "rule": rule,
            "parents": list(parent_ids),
            "derived_at": time.time(),
        }

        self.nodes[self.root_id].children.append(node_id)
        self.nodes[node_id] = node
        self._estimate_size()
        self._prune_if_needed()
        self.save_to_disk()
        return node_id

    def retrieve(
        self,
        node_id: str,
        consumer_id: str = DEFAULT_CONSUMER,
        min_coherence: float = 0.5,
        apply_temporal_decay: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve with coherence, consent, and optional temporal-decay enforcement."""
        if node_id not in self.nodes:
            return None

        node = self.nodes[node_id]
        apply_decay = (
            self.default_temporal_decay
            if apply_temporal_decay is None
            else apply_temporal_decay
        )

        # Consent enforcement first (don't leak coherence/staleness on denied data).
        if node.metadata.consent_flags == 0:
            self.registry._log(consumer_id, node_id, "denied")
            return {"status": "consent_denied"}
        if not self.registry.is_allowed(consumer_id, node.metadata.consent_flags):
            self.registry._log(consumer_id, node_id, "denied")
            return {"status": "consent_denied"}

        effective = self._effective_coherence(node, apply_decay)
        if effective < min_coherence:
            status = "data_stale" if apply_decay else "low_coherence"
            self.registry._log(consumer_id, node_id, status)
            return {
                "status": status,
                "summary": node.summary,
                "effective_coherence": round(effective, 4),
            }

        self.registry._log(consumer_id, node_id, "retrieve")

        # Symbolic (degraded) node — payload (if small enough to survive) still returned.
        if isinstance(node.content, dict) and node.content.get("type") == "symbolic":
            return {
                "id": node_id,
                "content": {"type": "symbolic", "hash": node.content["hash"]},
                "payload": node.payload,
                "metadata": node.metadata.to_dict(),
                "effective_coherence": round(effective, 4),
                "warning": "Tensor degraded to hash-only; payload (if any) preserved.",
            }

        if isinstance(node.content, SparseTensor):
            content = {
                "shape": node.content.shape,
                "values_sample": node.content.values[:10],
                "sparsity": node.content.sparsity,
                "quantized": node.content.quantized,
            }
        else:
            content = node.content

        return {
            "id": node_id,
            "content": content,
            "payload": node.payload,
            "metadata": node.metadata.to_dict(),
            "effective_coherence": round(effective, 4),
        }

    def verify(self, node_id: str, data: Any, payload: Optional[Any] = None) -> bool:
        """Verify that `data` (+ optional `payload`) matches the node's
        provenance hash. Pass the same payload that was supplied at encode time."""
        if node_id not in self.nodes:
            return False
        expected = self.nodes[node_id].metadata.provenance_hash
        return expected == self._payload_aware_hash(data, payload)

    # --- RAM profiling ------------------------------------------------------ #
    def _deep_size(self, obj: Any, seen: Optional[set] = None) -> int:
        """Recursive sys.getsizeof. For production Pi profiling, psutil RSS is
        a useful cross-check but is intentionally NOT a required dependency."""
        if seen is None:
            seen = set()
        oid = id(obj)
        if oid in seen:
            return 0
        seen.add(oid)
        size = sys.getsizeof(obj)
        if isinstance(obj, dict):
            for k, v in obj.items():
                size += self._deep_size(k, seen) + self._deep_size(v, seen)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                size += self._deep_size(item, seen)
        elif hasattr(obj, "__dict__"):
            size += self._deep_size(vars(obj), seen)
        return size

    def _estimate_size(self) -> None:
        total = self._deep_size(self.nodes) + self._deep_size(self.registry)
        self._current_size_estimate = total

    # --- Pruning ------------------------------------------------------------ #
    def _eviction_score(self, nid: str) -> float:
        m = self.nodes[nid].metadata
        # Apply decay to the score so stale data is preferentially evicted.
        effective = self._effective_coherence(self.nodes[nid], apply_decay=True)
        return effective * m.family_priority * m.temporal_weight

    def _prune_if_needed(self) -> None:
        """Evict lowest weighted-score nodes when over the RAM limit."""
        limit_bytes = self.max_ram_mb * 1024 * 1024
        guard = 0
        while self._current_size_estimate > limit_bytes and guard < len(self.nodes):
            guard += 1
            candidates = [nid for nid in self.nodes if nid != self.root_id]
            if not candidates:
                break
            candidates.sort(key=self._eviction_score)
            to_remove = candidates[0]
            score = self._eviction_score(to_remove)

            for n in self.nodes.values():
                if to_remove in n.children:
                    n.children.remove(to_remove)
            self.nodes.pop(to_remove, None)
            print(f"[CrystalMemory] Evicted {to_remove} (score: {score:.4f})")
            self._estimate_size()

    # --- Hierarchical summarization ----------------------------------------- #
    def summarize_children(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Aggregate child statistics into node.summary. Non-destructive."""
        if node_id not in self.nodes:
            return None
        node = self.nodes[node_id]
        if not node.children:
            return None

        coherences, shapes = [], []
        for child_id in node.children:
            child = self.nodes.get(child_id)
            if child is None:
                continue
            coherences.append(child.metadata.coherence_score)
            if isinstance(child.content, SparseTensor):
                shapes.append(list(child.content.shape))

        summary = {
            "num_children": len(node.children),
            "avg_coherence": round(sum(coherences) / len(coherences), 4) if coherences else 0.0,
            "child_shapes": shapes,
            "summarized_at": time.time(),
        }
        node.summary = summary
        self.save_to_disk()
        return summary

    def collapse_children(self, node_id: str, require_summary: bool = True) -> int:
        """Explicit, logged deletion of children after summarization.

        Returns number of children removed. Refuses to collapse without a
        summary when require_summary is True (the safe default).
        """
        if node_id not in self.nodes:
            return 0
        node = self.nodes[node_id]
        if require_summary and not node.summary:
            print(f"[CrystalMemory] collapse refused: {node_id} has no summary.")
            return 0

        removed = 0
        for child_id in list(node.children):
            if child_id in self.nodes:
                self.nodes.pop(child_id, None)
                removed += 1
            print(f"[CrystalMemory] Collapsed child {child_id} of {node_id}")
        node.children = []
        self._estimate_size()
        self.save_to_disk()
        return removed

    # --- Stats -------------------------------------------------------------- #
    def get_stats(self) -> Dict[str, Any]:
        total = len(self.nodes)
        avg = (
            sum(n.metadata.coherence_score for n in self.nodes.values()) / total
            if total else 0.0
        )
        symbolic = sum(
            1 for n in self.nodes.values()
            if isinstance(n.content, dict) and n.content.get("type") == "symbolic"
        )
        return {
            "total_nodes": total,
            "avg_coherence": round(avg, 3),
            "estimated_ram_mb": round(self._current_size_estimate / (1024 * 1024), 3),
            "root_children": len(self.nodes[self.root_id].children),
            "symbolic_nodes": symbolic,
            "registered_consumers": len(self.registry.consumers),
            "access_log_entries": len(self.registry.access_log),
            "last_status": self.last_status,
        }

    # --- Persistence (atomic + checksum) ------------------------------------ #
    def _serialize(self) -> Dict[str, Any]:
        nodes = {nid: node.to_dict() for nid, node in self.nodes.items()}
        nodes_str = json.dumps(nodes, sort_keys=True, ensure_ascii=False)
        checksum = hashlib.sha256(nodes_str.encode("utf-8")).hexdigest()
        return {
            "format_version": 2,
            "root_id": self.root_id,
            "coherence_threshold": self.coherence_threshold,
            "decay_half_life_days": self.decay_half_life_days,
            "registry": self.registry.to_dict(),
            "nodes": nodes,
            "checksum": checksum,
        }

    def _deserialize(self, data: Dict[str, Any]) -> None:
        # Integrity check (never crash on mismatch).
        stored_checksum = data.get("checksum")
        nodes_data = data.get("nodes", {})
        if stored_checksum is not None:
            nodes_str = json.dumps(nodes_data, sort_keys=True, ensure_ascii=False)
            expected = hashlib.sha256(nodes_str.encode("utf-8")).hexdigest()
            if expected != stored_checksum:
                print("[CrystalMemory] WARNING: checksum mismatch — "
                      "attempting best-effort recovery.")
                self.last_status = "checksum_mismatch_recovered"

        self.nodes.clear()
        self.root_id = data.get("root_id", "root")
        self.coherence_threshold = data.get("coherence_threshold", 0.6)
        self.decay_half_life_days = data.get(
            "decay_half_life_days", self.decay_half_life_days
        )

        reg_data = data.get("registry")
        if reg_data:
            self.registry = ConsumerRegistry.from_dict(reg_data)
        if self.DEFAULT_CONSUMER not in self.registry.consumers:
            self.registry.register(self.DEFAULT_CONSUMER, "Default User", permissions=0b1)

        recovered = 0
        for nid, nd in nodes_data.items():
            try:
                content = nd.get("content", {})
                if isinstance(content, dict) and "shape" in content:
                    content = SparseTensor.from_dict(content)
                meta = CoherenceMetadata.from_dict(nd.get("metadata", {}))
                self.nodes[nid] = HierarchicalNode(
                    id=nid,
                    content=content,
                    children=nd.get("children", []),
                    summary=nd.get("summary"),
                    metadata=meta,
                    payload=nd.get("payload"),  # None for pre-payload files
                )
                recovered += 1
            except Exception as e:
                # Best-effort: skip unparseable nodes rather than fail the load.
                print(f"[CrystalMemory] Skipped corrupt node {nid}: {e}")

        if self.root_id not in self.nodes:
            self.nodes[self.root_id] = HierarchicalNode(id=self.root_id, content={})

    def save_to_disk(self) -> bool:
        """Atomic write: temp file + os.replace. Safe for microSD."""
        tmp_path = self.storage_path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self._serialize(), f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self.storage_path)
            return True
        except Exception as e:
            print(f"[CrystalMemory] Save error: {e}")
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            return False

    def load_from_disk(self) -> bool:
        if not os.path.exists(self.storage_path):
            return False
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self._deserialize(raw)
            self._estimate_size()
            return True
        except json.JSONDecodeError as e:
            print(f"[CrystalMemory] Corrupt JSON ({e}); starting from empty state.")
            self.last_status = "load_failed_empty_state"
            return False
        except Exception as e:
            print(f"[CrystalMemory] Load error: {e}")
            self.last_status = "load_failed_empty_state"
            return False

    def _load_from_disk(self) -> None:
        self.load_from_disk()


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    mem = CrystalMemory(
        max_ram_mb=256,
        storage_path="crystal_memory_demo.json",
        decay_half_life_days=45.0,
    )

    mem.register_consumer("alice", "Alice", permissions=0b01)
    mem.register_consumer("family", "Family Shared", permissions=0b10)

    nid = mem.encode(
        [1.5, 0.0, 3.2, 0.0, 4.8] * 120,
        coherence_boost=0.93,
        consent_flags=0b01,      # User-only
        family_priority=1.1,
    )

    print("Encoded node:", nid)
    print("Stats:", json.dumps(mem.get_stats(), indent=2))
    print("Alice retrieve:", mem.retrieve(nid, consumer_id="alice"))
    print("Family retrieve:", mem.retrieve(nid, consumer_id="family"))
    print("Verify (correct data):", mem.verify(nid, [1.5, 0.0, 3.2, 0.0, 4.8] * 120))
    print("Verify (wrong data):", mem.verify(nid, [9.9]))
