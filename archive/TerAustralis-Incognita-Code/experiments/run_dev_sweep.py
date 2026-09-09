#!/usr/bin/env python3
"""H2 V0.1 development sweep — independent Candidate A / B parameter exploration.

Development partition only. Final seed family sealed.
Does not freeze a configuration. Does not evaluate the 1M dual gate.
Does not modify production CrystalCore.
Receiver fidelity (agreement with dense reference + gold accuracy) is
the ranking axis. Bandwidth is recorded, not gated.
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
    PRECISION,
    PROTOCOL_VERSION,
    SWEEP_LENGTHS,
    SWEEP_QUESTIONS_PER_LENGTH,
    WEIGHT_SEED,
)
from benchmarks.harness import run_item  # noqa: E402
from benchmarks.metrics import paired_ratio_lcb, wilson_lcb  # noqa: E402
from benchmarks.model import load_frozen_weights  # noqa: E402
from benchmarks.sweep_grids import grid_candidate_a, grid_candidate_b  # noqa: E402
from datasets.generator.corpus import generate_item  # noqa: E402

OUT_DIR = ROOT / "results" / "dev-sweep-v0.1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def make_primitive(system: str, cfg: dict | None = None):
    if system == "reference":
        mod = _load_module("h2_ref_sweep", ROOT / "reference" / "dense.py")
        return mod.DenseAttention()
    if system == "candidate_a":
        mod = _load_module(
            "h2_a_sweep",
            ROOT / "candidates" / "hierarchical-block-sparse" / "attention.py",
        )
        return mod.HierarchicalBlockSparse(cfg)
    if system == "candidate_b":
        mod = _load_module(
            "h2_b_sweep",
            ROOT / "candidates" / "content-addressed-retrieval" / "attention.py",
        )
        return mod.ContentAddressedRetrieval(cfg)
    raise SystemExit(f"unknown system {system}")


def _items(partition: str, lengths, n: int):
    for length in lengths:
        for i in range(n):
            yield generate_item(partition, length, i)


def run_reference(lengths, n, partition: str) -> dict:
    primitive = make_primitive("reference")
    weights = load_frozen_weights()
    rows = []
    t0 = time.time()
    for item in _items(partition, lengths, n):
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
                "bandwidth_total": result.bandwidth["total"],
            }
        )
    payload = {
        "protocol": PROTOCOL_VERSION,
        "partition": partition,
        "system": "reference",
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": time.time() - t0,
        "precision": PRECISION,
        "weight_seed": WEIGHT_SEED,
        "rows": rows,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "reference.json"
    path.write_text(json.dumps(payload))
    acc = sum(r["correct"] for r in rows) / len(rows)
    print(f"reference n={len(rows)} acc={acc:.4f} {time.time()-t0:.1f}s -> {path}")
    return payload


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
    for r in rows:
        by_class.setdefault(r["question_class"], []).append(r["correct"])
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
        "one_m_dual_gate_evaluated": False,
        "configuration_frozen": False,
    }


def run_grid(system: str, grid: list[dict], ref: dict, lengths, n, partition: str) -> dict:
    weights = load_frozen_weights()
    ref_rows = ref["rows"]
    results = []
    t_all = time.time()
    for ci, cfg in enumerate(grid):
        primitive = make_primitive(system, cfg)
        rows = []
        t0 = time.time()
        for item in _items(partition, lengths, n):
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
                    "bandwidth_total": result.bandwidth["total"],
                }
            )
        metrics = _score_rows(rows, ref_rows)
        rec = {
            "config_id": ci,
            "cfg": cfg,
            "elapsed_sec": time.time() - t0,
            **metrics,
        }
        results.append(rec)
        print(
            f"  {system} [{ci+1}/{len(grid)}] acc={metrics['gold_accuracy']:.4f} "
            f"agree={metrics['agreement_with_reference']:.4f} "
            f"bw/ref={metrics['bandwidth_ratio_vs_reference']:.4f} "
            f"{rec['elapsed_sec']:.1f}s cfg={cfg}",
            flush=True,
        )
    payload = {
        "protocol": PROTOCOL_VERSION,
        "partition": partition,
        "system": system,
        "n_per_length": n,
        "lengths": list(lengths),
        "elapsed_sec": time.time() - t_all,
        "grid_size": len(grid),
        "disclaimer": (
            "Development sweep. Not a configuration freeze. "
            "Not a 1M dual-gate decision. No performance claims."
        ),
        "results": results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{system}.json"
    path.write_text(json.dumps(payload))
    print(f"wrote {path}")
    return payload


def _rank(results: list[dict]) -> list[dict]:
    # Receiver fidelity is the sole ranking axis.
    return sorted(
        results,
        key=lambda r: (
            -r["agreement_with_reference"],
            -r["gold_accuracy"],
            r["bandwidth_ratio_vs_reference"] or 1.0,
        ),
    )


def assemble(a: dict, b: dict, ref: dict) -> None:
    a_rank = _rank(a["results"])
    b_rank = _rank(b["results"])
    summary = {
        "protocol": PROTOCOL_VERSION,
        "phase": "development-sweep",
        "partition": "development",
        "configuration_frozen": False,
        "one_m_dual_gate_evaluated": False,
        "ranking_axis": "receiver_fidelity = agreement with dense reference",
        "n_per_length": a["n_per_length"],
        "lengths": a["lengths"],
        "compute_envelope": {
            "reference_sec": ref.get("elapsed_sec"),
            "candidate_a_sec": a["elapsed_sec"],
            "candidate_b_sec": b["elapsed_sec"],
            "candidate_a_configs": a["grid_size"],
            "candidate_b_configs": b["grid_size"],
            "note": "Wall-clock on the experimental runner. Not a dollar BOM. Not hardware PMU.",
        },
        "candidate_a_ranked": [
            {k: r[k] for k in ("config_id", "cfg", "gold_accuracy", "agreement_with_reference", "quality_ratio_lcb", "bandwidth_ratio_vs_reference", "by_class")}
            for r in a_rank
        ],
        "candidate_b_ranked": [
            {k: r[k] for k in ("config_id", "cfg", "gold_accuracy", "agreement_with_reference", "quality_ratio_lcb", "bandwidth_ratio_vs_reference", "by_class")}
            for r in b_rank
        ],
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    def top_table(name: str, ranked: list[dict], k: int = 5) -> list[str]:
        lines = [
            f"### {name} — top {k} by receiver fidelity (not frozen)",
            "",
            "| rank | agree | gold acc | BW/ref | cfg |",
            "|---|---|---|---|---|",
        ]
        for i, r in enumerate(ranked[:k], 1):
            lines.append(
                f"| {i} | {r['agreement_with_reference']:.4f} | {r['gold_accuracy']:.4f} | "
                f"{r['bandwidth_ratio_vs_reference']:.4f} | `{r['cfg']}` |"
            )
        return lines

    lines = [
        "# H2 development sweep (V0.1)",
        "",
        "**Status:** Development partition · no configuration freeze · no performance claims",
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
        "Receiver fidelity (agreement with the dense reference on the development",
        "subsample) is the sole ranking axis. Bandwidth is recorded, not gated.",
        "Top-ranked configs are development observations, not selected finals.",
        "",
        f"Subsample: n = {a['n_per_length']} items per length, lengths = {a['lengths']}.",
        "Generator: development seed family, item indices `[0, n)`.",
        "Final seed family was not used. Production `core/` was not modified.",
        "",
        f"Compute envelope: reference {ref.get('elapsed_sec', 0):.1f}s; "
        f"A {a['elapsed_sec']:.1f}s / {a['grid_size']} configs; "
        f"B {b['elapsed_sec']:.1f}s / {b['grid_size']} configs.",
        "",
    ]
    lines += top_table("Candidate A (hierarchical block-sparse)", a_rank)
    lines += [""]
    lines += top_table("Candidate B (content-addressed retrieval)", b_rank)
    lines += [
        "",
        "Full ranked lists: `summary.json`. Item-level reference: `reference.json`.",
        "",
        "H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven.",
        "External / xAI pitch remains Hold.",
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
    p.add_argument("--n", type=int, default=SWEEP_QUESTIONS_PER_LENGTH)
    p.add_argument("--lengths", type=int, nargs="+", default=list(SWEEP_LENGTHS))
    p.add_argument("--partition", default="development")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.partition == "final":
        raise SystemExit("refusing to touch the final seed family")
    if args.selftest:
        args.n = 10
        args.lengths = [2048]
        print("SELFTEST sweep: n=10 L=2048 — not the development-sweep record")
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
        a = run_grid("candidate_a", grid_candidate_a(), ref, args.lengths, args.n, args.partition)
    if args.system in ("all", "candidate_b"):
        b = run_grid("candidate_b", grid_candidate_b(), ref, args.lengths, args.n, args.partition)
    if args.system == "all":
        assemble(a, b, ref)


if __name__ == "__main__":
    main()
