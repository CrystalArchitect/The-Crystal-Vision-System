#!/usr/bin/env python3
"""H2 V0.1 validation — independent Candidate A / B, validation partition.

Validation seed family only. Final seed family sealed.
Does not freeze a configuration. Does not evaluate the 1M dual gate.
Does not modify production CrystalCore.
Receiver fidelity is the measurement axis. Bandwidth is recorded, not gated.
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
    FIDELITY_LENGTHS,
    PRECISION,
    PROTOCOL_VERSION,
    QUESTIONS_PER_LENGTH,
    WEIGHT_SEED,
)
from benchmarks.harness import run_item  # noqa: E402
from benchmarks.metrics import paired_ratio_lcb, wilson_lcb  # noqa: E402
from benchmarks.model import load_frozen_weights  # noqa: E402
from benchmarks.validation_configs import (  # noqa: E402
    CANDIDATE_A_VALIDATION,
    CANDIDATE_B_VALIDATION,
)
from datasets.generator.corpus import generate_item  # noqa: E402

OUT_DIR = ROOT / "results" / "validation-v0.1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def make_primitive(system: str, cfg: dict | None = None):
    if system == "reference":
        mod = _load_module("h2_ref_val", ROOT / "reference" / "dense.py")
        return mod.DenseAttention()
    if system == "candidate_a":
        mod = _load_module(
            "h2_a_val",
            ROOT / "candidates" / "hierarchical-block-sparse" / "attention.py",
        )
        return mod.HierarchicalBlockSparse(cfg)
    if system == "candidate_b":
        mod = _load_module(
            "h2_b_val",
            ROOT / "candidates" / "content-addressed-retrieval" / "attention.py",
        )
        return mod.ContentAddressedRetrieval(cfg)
    raise SystemExit(f"unknown system {system}")


def _items(partition: str, lengths, n: int):
    for length in lengths:
        for i in range(n):
            yield generate_item(partition, length, i)


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
    return {
        "n": n,
        "gold_accuracy": gold_acc,
        "gold_accuracy_lcb": wilson_lcb(succ, n),
        "agreement_with_reference": agree / n if n else 0.0,
        "quality_ratio_vs_reference": (
            gold_acc / (sum(ref_correct) / n) if n and sum(ref_correct) else 0.0
        ),
        "quality_ratio_lcb": paired_ratio_lcb(cand_correct, ref_correct),
        "bandwidth_bytes": bw,
        "bandwidth_ratio_vs_reference": (bw / bw_ref) if bw_ref else None,
        "by_class": {k: sum(v) / len(v) for k, v in sorted(by_class.items())},
        "by_length": {k: sum(v) / len(v) for k, v in sorted(by_length.items())},
        "one_m_dual_gate_evaluated": False,
        "configuration_frozen": False,
    }


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


def run_reference(lengths, n, partition: str) -> dict:
    primitive = make_primitive("reference")
    weights = load_frozen_weights()
    rows = []
    t0 = time.time()
    for item in _items(partition, lengths, n):
        rows.append(_row(run_item(item, primitive, weights)))
    payload = {
        "protocol": PROTOCOL_VERSION,
        "phase": "validation",
        "partition": partition,
        "system": "reference",
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": time.time() - t0,
        "precision": PRECISION,
        "weight_seed": WEIGHT_SEED,
        "disclaimer": (
            "Validation. Not a configuration freeze. "
            "Not a 1M dual-gate decision. No performance claims."
        ),
        "rows": rows,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "reference.json"
    path.write_text(json.dumps(payload))
    acc = sum(r["correct"] for r in rows) / len(rows)
    print(f"reference n={len(rows)} acc={acc:.4f} {payload['elapsed_sec']:.1f}s -> {path}")
    return payload


def run_set(system: str, specs: list[dict], ref: dict, lengths, n, partition: str) -> dict:
    weights = load_frozen_weights()
    ref_rows = ref["rows"]
    results = []
    t_all = time.time()
    for ci, spec in enumerate(specs):
        primitive = make_primitive(system, spec["cfg"])
        rows = []
        t0 = time.time()
        for item in _items(partition, lengths, n):
            rows.append(_row(run_item(item, primitive, weights)))
        metrics = _score_rows(rows, ref_rows)
        rec = {
            "config_id": ci,
            "label": spec["label"],
            "cfg": spec["cfg"],
            "elapsed_sec": time.time() - t0,
            "rows": rows,
            **metrics,
        }
        results.append(rec)
        print(
            f"  {system} {spec['label']} acc={metrics['gold_accuracy']:.4f} "
            f"agree={metrics['agreement_with_reference']:.4f} "
            f"bw/ref={metrics['bandwidth_ratio_vs_reference']:.4f} "
            f"{rec['elapsed_sec']:.1f}s cfg={spec['cfg']}",
            flush=True,
        )
    payload = {
        "protocol": PROTOCOL_VERSION,
        "phase": "validation",
        "partition": partition,
        "system": system,
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": time.time() - t_all,
        "n_configs": len(specs),
        "disclaimer": (
            "Validation. Not a configuration freeze. "
            "Not a 1M dual-gate decision. No performance claims."
        ),
        "results": results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{system}.json"
    path.write_text(json.dumps(payload))
    print(f"wrote {path}")
    return payload


def assemble(a: dict, b: dict, ref: dict) -> None:
    def slim(results: list[dict]) -> list[dict]:
        keys = (
            "config_id",
            "label",
            "cfg",
            "gold_accuracy",
            "gold_accuracy_lcb",
            "agreement_with_reference",
            "quality_ratio_vs_reference",
            "quality_ratio_lcb",
            "bandwidth_ratio_vs_reference",
            "by_class",
            "by_length",
            "elapsed_sec",
        )
        return [{k: r[k] for k in keys} for r in results]

    ref_acc = sum(r["correct"] for r in ref["rows"]) / len(ref["rows"])
    summary = {
        "protocol": PROTOCOL_VERSION,
        "phase": "validation",
        "partition": "validation",
        "configuration_frozen": False,
        "one_m_dual_gate_evaluated": False,
        "ranking_axis": "receiver_fidelity = agreement with dense reference",
        "n_per_length": a["n_per_length"],
        "lengths": a["lengths"],
        "reference_gold_accuracy": ref_acc,
        "compute_envelope": {
            "reference_sec": ref.get("elapsed_sec"),
            "candidate_a_sec": a["elapsed_sec"],
            "candidate_b_sec": b["elapsed_sec"],
            "candidate_a_configs": a["n_configs"],
            "candidate_b_configs": b["n_configs"],
            "note": "Wall-clock on the experimental runner. Not a dollar BOM. Not hardware PMU.",
        },
        "candidate_a": slim(a["results"]),
        "candidate_b": slim(b["results"]),
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    def table(name: str, results: list[dict]) -> list[str]:
        lines = [
            f"### {name} (not frozen)",
            "",
            "| label | agree | gold acc | Q-ratio LCB | BW/ref | cfg |",
            "|---|---|---|---|---|---|",
        ]
        for r in results:
            lines.append(
                f"| {r['label']} | {r['agreement_with_reference']:.4f} | "
                f"{r['gold_accuracy']:.4f} | {r['quality_ratio_lcb']:.4f} | "
                f"{r['bandwidth_ratio_vs_reference']:.4f} | `{r['cfg']}` |"
            )
        return lines

    lines = [
        "# H2 validation (V0.1)",
        "",
        "**Status:** Validation partition · no configuration freeze · no performance claims",
        "",
        "## Interpretation Boundary",
        "",
        "This report does **not** demonstrate:",
        "",
        "- A frozen candidate configuration (GOVERNANCE step 4 has not occurred)",
        "- A 1M-token result, nor a dual-gate pass or fail",
        "- A language-model result (synthetic associative-memory encoder only)",
        "- Hardware bandwidth (analytical fp32 element counts only)",
        "- CrystalCore production quality or an xAI-relevant advantage",
        "- Anything about H1, Optimus, or brain-to-brain / non-local coupling",
        "",
        "Receiver fidelity (agreement with the dense reference on the validation",
        "partition) is the sole measurement axis. Bandwidth is recorded, not gated.",
        "Configs under test were taken from each candidate's own published sweep",
        "ranking plus the Step-1 development default. They are not selected finals.",
        "",
        f"n = {a['n_per_length']} items per length, lengths = {a['lengths']}.",
        "Generator: validation seed family. Development items were not reused.",
        "Final seed family was not used. Production `core/` was not modified.",
        "",
        f"Dense reference gold accuracy on this partition: {ref_acc:.4f}.",
        "",
        f"Compute envelope: reference {ref.get('elapsed_sec', 0):.1f}s; "
        f"A {a['elapsed_sec']:.1f}s / {a['n_configs']} configs; "
        f"B {b['elapsed_sec']:.1f}s / {b['n_configs']} configs.",
        "Not a dollar BOM.",
        "",
    ]
    lines += table("Candidate A (hierarchical block-sparse)", a["results"])
    lines += [""]
    lines += table("Candidate B (content-addressed retrieval)", b["results"])
    lines += [
        "",
        "Full metrics: `summary.json`. Item-level rows: `reference.json`,",
        "`candidate_a.json`, `candidate_b.json`.",
        "",
        "H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven.",
        "External / xAI pitch remains Hold.",
        "",
        "Locked next step, when ordered: configuration freeze (one config per",
        "candidate). Still not 1M.",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_DIR / 'summary.md'}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--system",
        choices=("reference", "candidate_a", "candidate_b", "all", "assemble"),
        default="all",
    )
    p.add_argument("--n", type=int, default=QUESTIONS_PER_LENGTH)
    p.add_argument("--lengths", type=int, nargs="+", default=list(FIDELITY_LENGTHS))
    p.add_argument("--partition", default="validation")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.partition == "final":
        raise SystemExit("refusing to touch the final seed family")
    if args.partition == "development":
        raise SystemExit(
            "validation must use the validation seed family; "
            "development items were already used in steps 1–2"
        )
    if args.selftest:
        args.n = 10
        args.lengths = [2048]
        print("SELFTEST validation: n=10 L=2048 — not the validation record")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.system == "assemble":
        a = json.loads((OUT_DIR / "candidate_a.json").read_text())
        b = json.loads((OUT_DIR / "candidate_b.json").read_text())
        ref = json.loads((OUT_DIR / "reference.json").read_text())
        assemble(a, b, ref)
        return
    if args.system in ("all", "reference"):
        ref = run_reference(args.lengths, args.n, args.partition)
    else:
        ref = json.loads((OUT_DIR / "reference.json").read_text())
    a = b = None
    if args.system in ("all", "candidate_a"):
        a = run_set(
            "candidate_a", CANDIDATE_A_VALIDATION, ref, args.lengths, args.n, args.partition
        )
    if args.system in ("all", "candidate_b"):
        b = run_set(
            "candidate_b", CANDIDATE_B_VALIDATION, ref, args.lengths, args.n, args.partition
        )
    if args.system == "all":
        assemble(a, b, ref)


if __name__ == "__main__":
    main()
