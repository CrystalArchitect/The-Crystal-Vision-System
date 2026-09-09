#!/usr/bin/env python3
"""H2 V0.1 reference-fidelity test at 32k / 64k.

Development partition only. Does not touch the final seed family.
Does not modify production CrystalCore. Makes no 1M-gate claims.

Candidates run independently: each writes its own result file before
the assembler reads them.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmarks.config import (  # noqa: E402
    CANDIDATE_A_DEV,
    CANDIDATE_B_DEV,
    FIDELITY_LENGTHS,
    PRECISION,
    PROTOCOL_VERSION,
    QUESTIONS_PER_LENGTH,
    WEIGHT_SEED,
)
from benchmarks.harness import run_item  # noqa: E402
from benchmarks.metrics import paired_ratio_lcb, wilson_lcb  # noqa: E402
from benchmarks.model import load_frozen_weights  # noqa: E402
from datasets.generator.corpus import generate_item  # noqa: E402

OUT_DIR = ROOT / "results" / "reference-fidelity-32k-64k"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def make_primitive(system: str):
    if system == "reference":
        mod = _load_module("h2_ref", ROOT / "reference" / "dense.py")
        return mod.DenseAttention()
    if system == "candidate_a":
        mod = _load_module(
            "h2_a",
            ROOT / "candidates" / "hierarchical-block-sparse" / "attention.py",
        )
        return mod.HierarchicalBlockSparse()
    if system == "candidate_b":
        mod = _load_module(
            "h2_b",
            ROOT / "candidates" / "content-addressed-retrieval" / "attention.py",
        )
        return mod.ContentAddressedRetrieval()
    raise SystemExit(f"unknown system {system}")


def run_system(system: str, lengths, n, partition: str) -> dict:
    primitive = make_primitive(system)
    weights = load_frozen_weights()
    rows = []
    t0 = time.time()
    for length in lengths:
        n_ok = 0
        for i in range(n):
            item = generate_item(partition, length, i)
            result = run_item(item, primitive, weights)
            rows.append(
                {
                    "item_id": result.item_id,
                    "length": result.length,
                    "question_class": result.question_class,
                    "bucket": result.bucket,
                    "pred_ids": list(result.pred_ids),
                    "gold_ids": list(result.gold_ids),
                    "correct": result.correct,
                    "bandwidth": result.bandwidth,
                }
            )
            n_ok += result.correct
            if (i + 1) % 25 == 0 or i + 1 == n:
                print(
                    f"  {system} L={length} {i+1}/{n} acc={n_ok/(i+1):.3f}",
                    flush=True,
                )
    elapsed = time.time() - t0
    payload = {
        "protocol": PROTOCOL_VERSION,
        "partition": partition,
        "system": system,
        "primitive": primitive.name,
        "precision": PRECISION,
        "weight_seed": WEIGHT_SEED,
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": elapsed,
        "candidate_a_dev": CANDIDATE_A_DEV if system == "candidate_a" else None,
        "candidate_b_dev": CANDIDATE_B_DEV if system == "candidate_b" else None,
        "disclaimer": (
            "Reference-fidelity measurements on the development partition. "
            "Not a 1M dual-gate decision. No performance claims."
        ),
        "rows": rows,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{system}.json"
    path.write_text(json.dumps(payload))
    print(f"wrote {path} ({len(rows)} items, {elapsed:.1f}s)")
    return payload


def assemble() -> None:
    ref = json.loads((OUT_DIR / "reference.json").read_text())
    a = json.loads((OUT_DIR / "candidate_a.json").read_text())
    b = json.loads((OUT_DIR / "candidate_b.json").read_text())
    systems = {"reference": ref, "candidate_a": a, "candidate_b": b}

    def bw_total(payload):
        return int(sum(r["bandwidth"]["total"] for r in payload["rows"]))

    summary = {
        "protocol": PROTOCOL_VERSION,
        "phase": "reference-fidelity-32k-64k",
        "partition": "development",
        "disclaimer": (
            "Measurements only. The 1M dual gate is not evaluated. "
            "Candidate configs are development defaults, not frozen. "
            "No performance claims. CrystalCore advantage remains unproven."
        ),
        "bandwidth_model": "analytical fp32 element counts over index/routing/kv/attention/output",
        "systems": {},
    }
    ref_correct = [r["correct"] for r in ref["rows"]]
    n_ref = len(ref["rows"])
    ref_acc = (sum(ref_correct) / n_ref) if n_ref else 0.0
    for name, payload in systems.items():
        rows = payload["rows"]
        succ = sum(r["correct"] for r in rows)
        n = len(rows)
        by = defaultdict(lambda: {"s": 0, "n": 0})
        for r in rows:
            key = f"L{r['length']}/{r['question_class']}/{r['bucket']}"
            by[key]["s"] += r["correct"]
            by[key]["n"] += 1
        entry = {
            "primitive": payload["primitive"],
            "n": n,
            "gold_accuracy": succ / n if n else 0.0,
            "gold_accuracy_lcb": wilson_lcb(succ, n),
            "bandwidth_bytes": bw_total(payload),
            "elapsed_sec": payload["elapsed_sec"],
            "slices": {
                k: {"acc": v["s"] / v["n"], "n": v["n"]} for k, v in sorted(by.items())
            },
        }
        if name != "reference":
            cand_correct = [r["correct"] for r in rows]
            agree = sum(
                int(x["pred_ids"] == y["pred_ids"])
                for x, y in zip(rows, ref["rows"])
            )
            entry["agreement_with_reference"] = agree / n if n else 0.0
            entry["quality_ratio_vs_reference"] = (
                (succ / n) / ref_acc if n and ref_acc else 0.0
            )
            entry["quality_ratio_lcb"] = paired_ratio_lcb(cand_correct, ref_correct)
            entry["bandwidth_ratio_vs_reference"] = (
                bw_total(payload) / bw_total(ref) if bw_total(ref) else None
            )
            entry["one_m_dual_gate_evaluated"] = False
        summary["systems"][name] = entry

    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    lines = [
        "# H2 reference-fidelity measurements (32k / 64k)",
        "",
        "**Status:** Development partition · methodology locked · no performance claims",
        "",
        summary["disclaimer"],
        "",
        "| System | Gold acc | LCB(acc) | vs ref (ratio LCB) | BW bytes | BW / ref | Agree with ref |",
        "|---|---|---|---|---|---|---|",
    ]
    for name in ("reference", "candidate_a", "candidate_b"):
        e = summary["systems"][name]
        if name == "reference":
            lines.append(
                f"| {name} | {e['gold_accuracy']:.4f} | {e['gold_accuracy_lcb']:.4f} | — | {e['bandwidth_bytes']} | 1.00 | — |"
            )
        else:
            lines.append(
                f"| {name} | {e['gold_accuracy']:.4f} | {e['gold_accuracy_lcb']:.4f} | {e['quality_ratio_vs_reference']:.4f} (LCB {e['quality_ratio_lcb']:.4f}) | {e['bandwidth_bytes']} | {e['bandwidth_ratio_vs_reference']:.4f} | {e['agreement_with_reference']:.4f} |"
            )
    lines += [
        "",
        "1M dual gate was **not** evaluated. These numbers are reference-fidelity",
        "observations at 32k/64k on the development seed family.",
        "",
        f"n = {QUESTIONS_PER_LENGTH} items per length unless this run overrode `--n`.",
        f"Default lengths = {list(FIDELITY_LENGTHS)}.",
        "Candidate hyperparameters: development defaults (not frozen).",
        "",
        "H1 remains frozen. Production `core/` was not modified.",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_DIR / 'summary.md'}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--system",
        choices=("reference", "candidate_a", "candidate_b", "all", "assemble"),
    )
    p.add_argument("--n", type=int, default=QUESTIONS_PER_LENGTH)
    p.add_argument("--lengths", type=int, nargs="+", default=list(FIDELITY_LENGTHS))
    p.add_argument("--partition", default="development")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.partition == "final":
        raise SystemExit("refusing to touch the final seed family")
    if args.selftest:
        args.n = 40
        args.lengths = [2048, 4096]
        args.system = args.system or "all"
        print("SELFTEST mode: n=40 lengths=2048,4096 — not the locked 32k/64k run")
    system = args.system or "all"
    if system == "assemble":
        assemble()
        return
    if system == "all":
        for s in ("reference", "candidate_a", "candidate_b"):
            run_system(s, args.lengths, args.n, args.partition)
        assemble()
        return
    run_system(system, args.lengths, args.n, args.partition)


if __name__ == "__main__":
    main()
