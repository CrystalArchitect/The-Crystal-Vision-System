import os
import sys
import json
import time
import tempfile

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_memory import (
    CrystalMemory,
    SparseTensor,
    CoherenceMetadata,
    ConsumerRegistry,
)


# --------------------------------------------------------------------------- #
# Metadata + tensor basics
# --------------------------------------------------------------------------- #
def test_coherence_metadata():
    meta = CoherenceMetadata(coherence_score=0.85, consent_flags=3)
    d = meta.to_dict()
    meta2 = CoherenceMetadata.from_dict(d)
    assert meta2.coherence_score == 0.85
    assert meta2.consent_flags == 3


def test_coherence_metadata_tolerates_legacy_keys():
    # Old files may carry fields this version no longer defines.
    d = {"coherence_score": 0.5, "consent_flags": 1, "obsolete_field": 123}
    meta = CoherenceMetadata.from_dict(d)
    assert meta.coherence_score == 0.5


def test_sparse_tensor():
    tensor = SparseTensor(shape=(5,), indices=[(0,), (2,)], values=[1.5, 3.2])
    assert tensor.sparsity == 0.4
    d = tensor.to_dict()
    tensor2 = SparseTensor.from_dict(d)
    assert tensor2.shape == (5,)
    assert tensor2.indices == [(0,), (2,)]


# --------------------------------------------------------------------------- #
# Quantization edge cases (kept strong)
# --------------------------------------------------------------------------- #
def test_quantization_edge_cases():
    # Empty
    t = SparseTensor(shape=(0,), indices=[], values=[])
    t.quantize()
    assert t.values == []
    assert t.quantized is True

    # Constant values
    t = SparseTensor(shape=(3,), indices=[(0,), (1,), (2,)], values=[5.0, 5.0, 5.0])
    t.quantize()
    assert t.scale == 1.0

    # Extreme range
    t = SparseTensor(shape=(2,), indices=[(0,), (1,)], values=[-1e9, 1e9])
    t.quantize(8)
    assert all(0 <= v <= 255 for v in t.values)

    # 4-bit
    t = SparseTensor(shape=(4,), indices=[(i,) for i in range(4)], values=[-10, -1, 1, 10])
    t.quantize(4)
    assert all(0 <= v <= 15 for v in t.values)


def test_dequantize_roundtrip_approx():
    original = [-10.0, -1.0, 1.0, 10.0]
    t = SparseTensor(shape=(4,), indices=[(i,) for i in range(4)], values=list(original))
    t.quantize(8)
    recovered = t.dequantize()
    # 8-bit over a range of 20 -> step ~0.078; allow generous tolerance.
    for o, r in zip(original, recovered):
        assert abs(o - r) < 0.2


# --------------------------------------------------------------------------- #
# Basic encode / retrieve
# --------------------------------------------------------------------------- #
def test_crystal_memory_basic(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    nid = mem.encode([1.0, 2.0, 0.0, 4.0], coherence_boost=0.9, consent_flags=1)
    result = mem.retrieve(nid)
    assert result is not None
    assert result["metadata"]["coherence_score"] > 0.7


def test_provenance_verification(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    data = [1.0, 2.0, 3.0]
    nid = mem.encode(data, consent_flags=1)
    assert mem.verify(nid, data) is True
    assert mem.verify(nid, [9.9, 9.9]) is False


# --------------------------------------------------------------------------- #
# Consent + coherence filters
# --------------------------------------------------------------------------- #
def test_consent_and_coherence_filters(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))

    nid = mem.encode([1, 2, 3], consent_flags=0)
    assert mem.retrieve(nid)["status"] == "consent_denied"

    nid2 = mem.encode([1, 2, 3], coherence_boost=0.3, consent_flags=1)
    assert mem.retrieve(nid2, min_coherence=0.8)["status"] == "low_coherence"


# --------------------------------------------------------------------------- #
# Consumer access control (NEW)
# --------------------------------------------------------------------------- #
def test_consumer_access_control(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    mem.register_consumer("bob", "Bob", permissions=0b10)

    # Data flagged for bit 0 (Alice) only.
    nid = mem.encode([1, 2, 3], consent_flags=0b01)

    assert mem.retrieve(nid, consumer_id="alice").get("status") != "consent_denied"
    assert mem.retrieve(nid, consumer_id="bob")["status"] == "consent_denied"


def test_unknown_consumer_denied(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    nid = mem.encode([1, 2, 3], consent_flags=0b01)
    assert mem.retrieve(nid, consumer_id="ghost")["status"] == "consent_denied"


def test_revocation_without_deletion(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    nid = mem.encode([1, 2, 3], consent_flags=0b01)

    assert mem.retrieve(nid, consumer_id="alice").get("status") != "consent_denied"
    mem.revoke_consumer("alice")
    assert mem.retrieve(nid, consumer_id="alice")["status"] == "consent_denied"
    # Data still exists (default consumer can't see bit 0b01 either unless flagged)
    assert nid in mem.nodes


def test_access_log_records_events(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    nid = mem.encode([1, 2, 3], consent_flags=0b01)

    mem.retrieve(nid, consumer_id="alice")          # retrieve
    mem.retrieve(nid, consumer_id="ghost")          # denied

    actions = [e["action"] for e in mem.registry.access_log]
    assert "retrieve" in actions
    assert "denied" in actions


def test_access_log_is_bounded(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    mem.registry.max_log_entries = 100
    mem.register_consumer("alice", "Alice", permissions=0b01)
    nid = mem.encode([1, 2, 3], consent_flags=0b01)
    for _ in range(500):
        mem.retrieve(nid, consumer_id="alice")
    assert len(mem.registry.access_log) <= 100


# --------------------------------------------------------------------------- #
# Temporal decay (NEW)
# --------------------------------------------------------------------------- #
def test_temporal_decay_marks_stale(tmp_path):
    mem = CrystalMemory(
        max_ram_mb=50,
        storage_path=str(tmp_path / "m.json"),
        decay_half_life_days=30.0,
    )
    nid = mem.encode([1, 2, 3], coherence_boost=0.9, consent_flags=1)

    # Fresh: high coherence, retrievable.
    fresh = mem.retrieve(nid, apply_temporal_decay=True)
    assert "effective_coherence" in fresh
    assert fresh.get("status") != "data_stale"

    # Age the node 60 days (two half-lives -> ~0.25 multiplier).
    mem.nodes[nid].metadata.timestamp = time.time() - (60 * 86400)
    stale = mem.retrieve(nid, apply_temporal_decay=True, min_coherence=0.5)
    assert stale["status"] == "data_stale"
    assert stale["effective_coherence"] < 0.5


def test_temporal_decay_off_by_default(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    nid = mem.encode([1, 2, 3], coherence_boost=0.9, consent_flags=1)
    mem.nodes[nid].metadata.timestamp = time.time() - (365 * 86400)
    # No decay requested -> old data still valid.
    result = mem.retrieve(nid)
    assert result.get("status") not in ("data_stale",)


def test_instance_default_decay(tmp_path):
    mem = CrystalMemory(
        max_ram_mb=50,
        storage_path=str(tmp_path / "m.json"),
        decay_half_life_days=30.0,
        default_temporal_decay=True,
    )
    nid = mem.encode([1, 2, 3], coherence_boost=0.9, consent_flags=1)
    mem.nodes[nid].metadata.timestamp = time.time() - (120 * 86400)
    result = mem.retrieve(nid, min_coherence=0.5)  # uses instance default
    assert result["status"] == "data_stale"


# --------------------------------------------------------------------------- #
# Weighted pruning (NEW)
# --------------------------------------------------------------------------- #
def test_pruning_occurs(tmp_path):
    # ~3 KB/node; a 0.05 MB (~50 KB) budget forces eviction after ~15 nodes.
    mem = CrystalMemory(max_ram_mb=0.05, storage_path=str(tmp_path / "m.json"))
    for i in range(200):
        mem.encode([float(i)] * 30, coherence_boost=0.5, consent_flags=1)
    stats = mem.get_stats()
    assert stats["estimated_ram_mb"] <= 0.08  # Stayed near the limit
    assert stats["total_nodes"] < 200          # Eviction occurred


def test_pruning_respects_family_priority(tmp_path):
    # ~0.05 MB budget keeps roughly a dozen nodes alive — enough to observe
    # that priority, not raw coherence, decides who survives.
    mem = CrystalMemory(max_ram_mb=0.05, storage_path=str(tmp_path / "m.json"))

    protected = mem.encode(
        [1.0] * 20, coherence_boost=0.25, family_priority=50.0, consent_flags=1
    )
    sacrificial = mem.encode(
        [2.0] * 20, coherence_boost=0.9, family_priority=0.01, consent_flags=1
    )

    # Flood with medium-priority nodes to force eviction.
    for i in range(150):
        mem.encode([float(i)] * 30, coherence_boost=0.5,
                   family_priority=1.0, consent_flags=1)

    # High-priority node should outlive the low-priority high-coherence one.
    assert protected in mem.nodes
    assert sacrificial not in mem.nodes


# --------------------------------------------------------------------------- #
# Graceful degradation (NEW)
# --------------------------------------------------------------------------- #
def test_symbolic_fallback_on_memory_error(tmp_path, monkeypatch):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))

    # Force the tensor builder to raise MemoryError.
    def boom(*args, **kwargs):
        raise MemoryError("simulated pressure")

    monkeypatch.setattr(mem, "_build_tensor", boom)

    nid = mem.encode([1, 2, 3], coherence_boost=0.9, consent_flags=1)
    node = mem.nodes[nid]
    assert isinstance(node.content, dict)
    assert node.content["type"] == "symbolic"
    assert mem.last_status == "degraded_symbolic"

    # Symbolic nodes cap coherence at 0.3, so retrieve with a low threshold.
    result = mem.retrieve(nid, min_coherence=0.0)
    assert result["content"]["type"] == "symbolic"
    assert "warning" in result
    # Symbolic node coherence is capped low.
    assert node.metadata.coherence_score <= 0.3


# --------------------------------------------------------------------------- #
# Persistence: atomic + checksum + corruption recovery (NEW)
# --------------------------------------------------------------------------- #
def test_persistence(tmp_path):
    path = str(tmp_path / "test_memory.json")
    mem = CrystalMemory(max_ram_mb=50, storage_path=path)
    nid = mem.encode([10, 20, 30], consent_flags=3)
    mem.save_to_disk()

    mem2 = CrystalMemory(max_ram_mb=50, storage_path=path)
    result = mem2.retrieve(nid, min_coherence=0.0)
    assert result is not None
    assert result["metadata"]["consent_flags"] == 3


def test_atomic_save_leaves_no_tmp(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=50, storage_path=path)
    mem.encode([1, 2, 3], consent_flags=1)
    assert os.path.exists(path)
    assert not os.path.exists(path + ".tmp")


def test_checksum_present_in_file(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=50, storage_path=path)
    mem.encode([1, 2, 3], consent_flags=1)
    with open(path) as f:
        data = json.load(f)
    assert "checksum" in data
    assert len(data["checksum"]) == 64  # SHA-256 hex


def test_corruption_recovery_truncated(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=50, storage_path=path)
    mem.encode([1, 2, 3], consent_flags=3)

    # Truncate the file to simulate a partial write.
    with open(path, "r") as f:
        content = f.read()
    with open(path, "w") as f:
        f.write(content[:40])

    # Should not crash; should degrade to empty state cleanly.
    mem2 = CrystalMemory(max_ram_mb=50, storage_path=path)
    stats = mem2.get_stats()
    assert stats["total_nodes"] >= 1  # at least root
    assert mem2.last_status == "load_failed_empty_state"


def test_checksum_mismatch_flagged(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=50, storage_path=path)
    mem.encode([1, 2, 3], consent_flags=3)

    # Tamper with a node value but leave the (now-stale) checksum.
    with open(path) as f:
        data = json.load(f)
    # Mutate one node's coherence to invalidate the checksum.
    for nid, nd in data["nodes"].items():
        if nid != "root":
            nd["metadata"]["coherence_score"] = 0.123456
            break
    with open(path, "w") as f:
        json.dump(data, f)

    mem2 = CrystalMemory(max_ram_mb=50, storage_path=path)
    # Recovers (best-effort) and flags the mismatch.
    assert mem2.last_status == "checksum_mismatch_recovered"


# --------------------------------------------------------------------------- #
# Hierarchical summarization (NEW)
# --------------------------------------------------------------------------- #
def test_summarize_children_non_destructive(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    for i in range(3):
        mem.encode([float(i)] * 5, coherence_boost=0.8, consent_flags=1)

    summary = mem.summarize_children("root")
    assert summary is not None
    assert summary["num_children"] == 3
    assert 0.0 <= summary["avg_coherence"] <= 1.0
    # Children NOT deleted by summarization.
    assert len(mem.nodes["root"].children) == 3


def test_collapse_requires_summary(tmp_path):
    mem = CrystalMemory(max_ram_mb=50, storage_path=str(tmp_path / "m.json"))
    for i in range(3):
        mem.encode([float(i)] * 5, coherence_boost=0.8, consent_flags=1)

    # Refuses without a summary.
    removed = mem.collapse_children("root", require_summary=True)
    assert removed == 0
    assert len(mem.nodes["root"].children) == 3

    # After summarizing, collapse is allowed and logged.
    mem.summarize_children("root")
    removed = mem.collapse_children("root", require_summary=True)
    assert removed == 3
    assert len(mem.nodes["root"].children) == 0


# --------------------------------------------------------------------------- #
# RAM profiling sanity
# --------------------------------------------------------------------------- #
def test_real_ram_estimate_grows(tmp_path):
    mem = CrystalMemory(max_ram_mb=256, storage_path=str(tmp_path / "m.json"))
    baseline = mem._current_size_estimate
    for i in range(20):
        mem.encode([float(j) for j in range(50)], coherence_boost=0.5, consent_flags=1)
    assert mem._current_size_estimate > baseline


# --------------------------------------------------------------------------- #
# Durable payload (NEW)
# --------------------------------------------------------------------------- #
def test_payload_string_survives_roundtrip(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    text = "Draft policy: families retain data sovereignty by default."
    nid = mem.encode([0.0], coherence_boost=0.9, consent_flags=1, payload=text)

    # Reload from disk -> payload intact.
    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    result = mem2.retrieve(nid, min_coherence=0.0)
    assert result["payload"] == text


def test_payload_dict_survives_roundtrip(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    decision = {"type": "family_decision", "choice": "move", "votes": 3}
    nid = mem.encode([0.0], coherence_boost=0.9, consent_flags=1, payload=decision)

    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    result = mem2.retrieve(nid, min_coherence=0.0)
    assert result["payload"] == decision


def test_payload_aware_verification(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    text = "creative fragment: the river remembers every stone"
    nid = mem.encode([0.0], coherence_boost=0.9, consent_flags=1, payload=text)

    assert mem.verify(nid, [0.0], payload=text) is True
    assert mem.verify(nid, [0.0], payload="tampered text") is False


def test_node_without_payload_defaults_none(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    nid = mem.encode([1.0, 2.0, 3.0], coherence_boost=0.9, consent_flags=1)
    result = mem.retrieve(nid)
    assert result["payload"] is None


def test_backward_compat_pre_payload_file(tmp_path):
    """A file written without the payload field must still load cleanly."""
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    nid = mem.encode([1.0, 2.0], coherence_boost=0.9, consent_flags=1)

    # Simulate an old file: strip the 'payload' key from every node.
    with open(path) as f:
        data = json.load(f)
    for nd in data["nodes"].values():
        nd.pop("payload", None)
    # Recompute checksum so this looks like a legitimate older-but-intact file.
    nodes_str = json.dumps(data["nodes"], sort_keys=True, ensure_ascii=False)
    import hashlib
    data["checksum"] = hashlib.sha256(nodes_str.encode("utf-8")).hexdigest()
    with open(path, "w") as f:
        json.dump(data, f)

    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    result = mem2.retrieve(nid, min_coherence=0.0)
    assert result is not None
    assert result["payload"] is None  # gracefully absent
    assert mem2.last_status != "checksum_mismatch_recovered"


def test_encode_derived_routes_nonnumeric_to_payload(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    a = mem.encode([1.0], coherence_boost=0.9, consent_flags=1)
    # Pass a string directly as 'data' -> should be routed to payload.
    nid = mem.encode_derived(
        data="conclusion: proceed with option B",
        parent_ids=[a],
        coherence=0.7,
        consent_flags=1,
        rule="synthesize",
    )
    result = mem.retrieve(nid, min_coherence=0.0)
    assert result["payload"] == "conclusion: proceed with option B"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
