#!/usr/bin/env python3
"""H2 V0.1 immutable final test — GOVERNANCE step 5.

Frozen configs only + dense reference. Final seed family, unsealed here only.
Dual-gate evaluated at 1M tokens. Production core/ unmodified.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmarks.config import (  # noqa: E402
    FINAL_LENGTHS,
    PRECISION,
    PROTOCOL_VERSION,
    QUESTIONS_PER_LENGTH,
    WEIGHT_SEED,
)
from benchmarks.frozen_configs import (  # noqa: E402
    CANDIDATE_A_FROZEN,
    CANDIDATE_B_FROZEN,
)
from benchmarks.harness import run_item  # noqa: E402
from benchmarks.metrics import paired_ratio_lcb, wilson_lcb  # noqa: E402
from benchmarks.model import load_frozen_weights  # noqa: E402
from datasets.generator.corpus import generate_item  # noqa: E402
from datasets.generator.seeds import allow_final_seed_family  # noqa: E402

OUT_DIR = ROOT / "results" / "final-test-v0.1"
ONE_M = 1_048_576
QUALITY_GATE = 0.90
BANDWIDTH_GATE = 0.40


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def make_primitive(system: str, cfg: dict | None = None):
    if system == "reference":
        mod = _load_module("h2_ref_final", ROOT / "reference" / "dense.py")
        return mod.DenseAttention()
    if system == "candidate_a":
        mod = _load_module(
            "h2_a_final",
            ROOT / "candidates" / "hierarchical-block-sparse" / "attention.py",
        )
        return mod.HierarchicalBlockSparse(cfg)
    if system == "candidate_b":
        mod = _load_module(
            "h2_b_final",
            ROOT / "candidates" / "content-addressed-retrieval" / "attention.py",
        )
        return mod.ContentAddressedRetrieval(cfg)
    raise SystemExit(f"unknown system {system}")


def _row(result) -> dict:
    return {
        "item_id": result.item_id,
        "length": result.length,
        "question_class": result.question_class,
        "bucket": result.bucket,
        "pred_ids": list(result.pred_ids),
        "gold_ids": list(result.gold_ids),
        "correct": result.correct,
        "bandwidth_total": result.bandwidth["total"],
    }


def _score_rows(rows, ref_rows) -> dict:
    n = len(rows)
    succ = sum(r["correct"] for r in rows)
    gold_acc = succ / n if n else 0.0
    agree = sum(int(a["pred_ids"] == b["pred_ids"]) for a, b in zip(rows, ref_rows))
    ref_correct = [r["correct"] for r in ref_rows]
    cand_correct = [r["correct"] for r in rows]
    bw = int(sum(r["bandwidth_total"] for r in rows))
    bw_ref = int(sum(r["bandwidth_total"] for r in ref_rows))
    by_class: dict[str, list[int]] = {}
    by_length: dict[str, list[int]] = {}
    for r in rows:
        by_class.setdefault(r["question_class"], []).append(r["correct"])
        by_length.setdefault(str(r["length"]), []).append(r["correct"])
    q_lcb = paired_ratio_lcb(cand_correct, ref_correct)
    bw_ratio = (bw / bw_ref) if bw_ref else None
    return {
        "n": n,
        "gold_accuracy": gold_acc,
        "gold_accuracy_lcb": wilson_lcb(succ, n),
        "agreement_with_reference": agree / n if n else 0.0,
        "quality_ratio_vs_reference": (
            gold_acc / (sum(ref_correct) / n) if n and sum(ref_correct) else 0.0
        ),
        "quality_ratio_lcb": q_lcb,
        "bandwidth_bytes": bw,
        "bandwidth_ratio_vs_reference": bw_ratio,
        "by_class": {k: sum(v) / len(v) for k, v in sorted(by_class.items())},
        "by_length": {k: sum(v) / len(v) for k, v in sorted(by_length.items())},
    }


def _gate(metrics: dict) -> dict:
    if metrics.get("n", 0) <= 0:
        return {
            "quality_gate": QUALITY_GATE,
            "bandwidth_gate": BANDWIDTH_GATE,
            "quality_ratio_lcb": None,
            "bandwidth_ratio_vs_reference": None,
            "quality_pass": False,
            "bandwidth_pass": False,
            "dual_gate": "inconclusive",
            "simultaneous": False,
            "reason": "no 1M items in this run",
        }
    q = float(metrics["quality_ratio_lcb"])
    bw = metrics["bandwidth_ratio_vs_reference"]
    bw_v = float(bw) if bw is not None else None
    q_pass = q >= QUALITY_GATE
    bw_pass = bw_v is not None and bw_v <= BANDWIDTH_GATE
    if bw_v is None:
        decision = "inconclusive"
    elif q_pass and bw_pass:
        decision = "pass"
    else:
        decision = "fail"
    return {
        "quality_gate": QUALITY_GATE,
        "bandwidth_gate": BANDWIDTH_GATE,
        "quality_ratio_lcb": q,
        "bandwidth_ratio_vs_reference": bw_v,
        "quality_pass": q_pass,
        "bandwidth_pass": bw_pass,
        "dual_gate": decision,
        "simultaneous": q_pass and bw_pass,
    }


def _ckpt(system: str, length: int) -> Path:
    return OUT_DIR / "checkpoints" / f"{system}_{length}.json"


def _run_length(system: str, primitive, weights, length: int, n: int, partition: str) -> list[dict]:
    path = _ckpt(system, length)
    if path.exists():
        payload = json.loads(path.read_text())
        if payload.get("n") == n and len(payload.get("rows", [])) == n:
            print(f"  resume {system} L={length} n={n}", flush=True)
            return payload["rows"]
    rows = []
    t0 = time.time()
    for i in range(n):
        item = generate_item(partition, length, i)
        rows.append(_row(run_item(item, primitive, weights)))
        if (i + 1) % 50 == 0 or i + 1 == n:
            acc = sum(r["correct"] for r in rows) / len(rows)
            print(
                f"  {system} L={length} {i+1}/{n} acc={acc:.4f} "
                f"{time.time() - t0:.1f}s",
                flush=True,
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"system": system, "length": length, "n": n, "rows": rows})
    )
    return rows


def run_system(system: str, cfg: dict | None, lengths, n: int, partition: str) -> dict:
    primitive = make_primitive(system, cfg)
    weights = load_frozen_weights()
    t0 = time.time()
    rows = []
    for length in lengths:
        rows.extend(_run_length(system, primitive, weights, length, n, partition))
    payload = {
        "protocol": PROTOCOL_VERSION,
        "phase": "immutable-final-test",
        "partition": partition,
        "system": system,
        "cfg": cfg,
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": time.time() - t0,
        "precision": PRECISION,
        "weight_seed": WEIGHT_SEED,
        "disclaimer": (
            "Immutable final test. Frozen configs only. Dual-gate evaluated at 1M. "
            "Synthetic associative-memory encoder. Analytical bandwidth. "
            "No performance claims beyond this locked record."
        ),
        "rows": rows,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{system}.json"
    path.write_text(json.dumps(payload))
    acc = sum(r["correct"] for r in rows) / len(rows)
    print(f"{system} n={len(rows)} acc={acc:.4f} {payload['elapsed_sec']:.1f}s -> {path}", flush=True)
    return payload


def _subset(rows: list[dict], length: int | None) -> list[dict]:
    if length is None:
        return rows
    return [r for r in rows if r["length"] == length]


def assemble(ref: dict, a: dict, b: dict) -> None:
    ref_rows = ref["rows"]
    systems = []
    for name, payload, cfg in (
        ("candidate_a", a, CANDIDATE_A_FROZEN),
        ("candidate_b", b, CANDIDATE_B_FROZEN),
    ):
        overall = _score_rows(payload["rows"], ref_rows)
        at_1m = _score_rows(_subset(payload["rows"], ONE_M), _subset(ref_rows, ONE_M))
        per_length = {}
        for L in payload["lengths"]:
            per_length[str(L)] = _score_rows(_subset(payload["rows"], L), _subset(ref_rows, L))
        rec = {
            "system": name,
            "cfg": cfg,
            "overall": overall,
            "per_length": per_length,
            "at_1M": at_1m,
            "dual_gate_1M": _gate(at_1m),
            "elapsed_sec": payload["elapsed_sec"],
        }
        systems.append(rec)

    ref_acc = sum(r["correct"] for r in ref_rows) / len(ref_rows)
    ref_1m = _subset(ref_rows, ONE_M)
    ref_1m_acc = sum(r["correct"] for r in ref_1m) / len(ref_1m) if ref_1m else None
    one_m_present = bool(ref_1m)
    summary = {
        "protocol": PROTOCOL_VERSION,
        "phase": "immutable-final-test",
        "partition": "final",
        "configuration_frozen": True,
        "one_m_dual_gate_evaluated": True,
        "n_per_length": ref["n_per_length"],
        "lengths": ref["lengths"],
        "reference_gold_accuracy": ref_acc,
        "reference_gold_accuracy_1M": ref_1m_acc,
        "quality_gate": QUALITY_GATE,
        "bandwidth_gate": BANDWIDTH_GATE,
        "compute_envelope": {
            "reference_sec": ref.get("elapsed_sec"),
            "candidate_a_sec": a["elapsed_sec"],
            "candidate_b_sec": b["elapsed_sec"],
            "note": "Wall-clock on the experimental runner. Not a dollar BOM. Not hardware PMU.",
        },
        "candidate_a": systems[0],
        "candidate_b": systems[1],
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    def gate_line(rec: dict) -> str:
        g = rec["dual_gate_1M"]
        if g["dual_gate"] == "inconclusive":
            return "INCONCLUSIVE (1M subset absent from this run)"
        return (
            f"{g['dual_gate'].upper()} "
            f"(quality LCB {g['quality_ratio_lcb']:.4f} "
            f"{'≥' if g['quality_pass'] else '<'} {QUALITY_GATE}; "
            f"BW/ref {g['bandwidth_ratio_vs_reference']:.4f} "
            f"{'≤' if g['bandwidth_pass'] else '>'} {BANDWIDTH_GATE})"
        )

    lines = [
        "# H2 immutable final test (V0.1)",
        "",
        "**Status:** GOVERNANCE step 5 recorded · dual-gate evaluated at 1M · no extra claims",
        "",
        "## Interpretation Boundary",
        "",
        "This report does **not** demonstrate:",
        "",
        "- Language-model quality (synthetic associative-memory encoder only)",
        "- Hardware bandwidth or dollar cost (analytical fp32 element counts only)",
        "- CrystalCore production quality, Optimus-relevance, or an xAI-relevant advantage",
        "- Anything about H1",
        "- Non-local, dimensional, or brain-to-brain information transfer",
        "- That a failed or passed 1M gate on this encoder transfers to any other task",
        "",
        "The dual gate is evaluated **only** on the 1M-token final-partition subset.",
        "Shorter lengths are a scaling record, not the gate. Candidates were scored",
        "independently against the dense reference. Production `core/` unmodified.",
        "",
        f"n = {ref['n_per_length']} items per length, lengths = {ref['lengths']}.",
        "Generator: final seed family (unsealed for this run only).",
        "",
        f"Dense reference gold accuracy (all lengths): {ref_acc:.4f}.",
        (
            f"Dense reference gold accuracy at 1M: {ref_1m_acc:.4f}."
            if one_m_present
            else "Dense reference gold accuracy at 1M: n/a (1M length not in this run)."
        ),
        "",
        f"Compute envelope: reference {ref.get('elapsed_sec', 0):.1f}s; "
        f"A {a['elapsed_sec']:.1f}s; B {b['elapsed_sec']:.1f}s. Not a dollar BOM.",
        "",
        "## Dual-gate at 1M (locked hypothesis)",
        "",
        f"LCB(Q_primitive / Q_full) ≥ {QUALITY_GATE} **and** "
        f"BW_primitive / BW_full ≤ {BANDWIDTH_GATE}, simultaneously.",
        "",
        f"- Candidate A: **{gate_line(systems[0])}**",
        f"- Candidate B: **{gate_line(systems[1])}**",
        "",
        "## Frozen configs under test",
        "",
        f"- Dense reference: full attention",
        f"- Candidate A: `{CANDIDATE_A_FROZEN}`",
        f"- Candidate B: `{CANDIDATE_B_FROZEN}`",
        "",
        "## Per-length record",
        "",
        "| length | ref acc | A agree | A Q-LCB | A BW/ref | B agree | B Q-LCB | B BW/ref |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for L in ref["lengths"]:
        ra = sum(r["correct"] for r in _subset(ref_rows, L)) / ref["n_per_length"]
        am = systems[0]["per_length"][str(L)]
        bm = systems[1]["per_length"][str(L)]
        lines.append(
            f"| {L} | {ra:.4f} | {am['agreement_with_reference']:.4f} | "
            f"{am['quality_ratio_lcb']:.4f} | {am['bandwidth_ratio_vs_reference']:.4f} | "
            f"{bm['agreement_with_reference']:.4f} | {bm['quality_ratio_lcb']:.4f} | "
            f"{bm['bandwidth_ratio_vs_reference']:.4f} |"
        )
    lines += [
        "",
        "Machine record: `summary.json`. Item-level rows: `reference.json`,",
        "`candidate_a.json`, `candidate_b.json`.",
        "",
        "H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven",
        "until a separate, later decision — not implied by this gate.",
        "External / xAI pitch remains Hold unless the steward changes it.",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_DIR / 'summary.md'}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--system",
        choices=("reference", "candidate_a", "candidate_b", "all", "assemble"),
        default="all",
    )
    p.add_argument("--n", type=int, default=QUESTIONS_PER_LENGTH)
    p.add_argument("--lengths", type=int, nargs="+", default=list(FINAL_LENGTHS))
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    allow_final_seed_family()
    global OUT_DIR
    if args.selftest:
        args.n = 8
        args.lengths = [2048, 4096]
        OUT_DIR = ROOT / "results" / "final-test-v0.1" / "_selftest"
        print("SELFTEST final: n=8 L=2048,4096 — not the locked record", flush=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    partition = "final"
    if args.system == "assemble":
        a = json.loads((OUT_DIR / "candidate_a.json").read_text())
        b = json.loads((OUT_DIR / "candidate_b.json").read_text())
        ref = json.loads((OUT_DIR / "reference.json").read_text())
        assemble(ref, a, b)
        return
    ref = a = b = None
    if args.system in ("all", "reference"):
        ref = run_system("reference", None, args.lengths, args.n, partition)
    else:
        ref_path = OUT_DIR / "reference.json"
        if ref_path.exists():
            ref = json.loads(ref_path.read_text())
    if args.system in ("all", "candidate_a"):
        a = run_system("candidate_a", CANDIDATE_A_FROZEN, args.lengths, args.n, partition)
    if args.system in ("all", "candidate_b"):
        b = run_system("candidate_b", CANDIDATE_B_FROZEN, args.lengths, args.n, partition)
    if args.system == "all":
        assemble(ref, a, b)
    elif args.system == "candidate_a" and ref is not None and (OUT_DIR / "candidate_b.json").exists():
        b = json.loads((OUT_DIR / "candidate_b.json").read_text())
        assemble(ref, a, b)
    elif args.system == "candidate_b" and ref is not None and (OUT_DIR / "candidate_a.json").exists():
        a = json.loads((OUT_DIR / "candidate_a.json").read_text())
        assemble(ref, a, b)


if __name__ == "__main__":
    main()
