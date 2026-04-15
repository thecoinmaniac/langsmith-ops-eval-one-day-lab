from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"

# Metric-specific pass thresholds. Unknown metrics default to 1.0.
PASS_THRESHOLDS: dict[str, float] = {
    "format_length": 1.0,
    "section_coverage": 1.0,
    "must_include": 0.67,
    "operational_specificity": 0.5,
    "semantic_theme_alignment": 0.5,
}


def load_experiment_report(experiment_name: str, reports_dir: Path | None = None) -> dict[str, Any]:
    base = reports_dir or REPORTS_DIR
    path = base / f"{experiment_name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Experiment report not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_experiment(report: dict[str, Any]) -> dict[str, Any]:
    results = report.get("results", []) or []
    metrics: dict[str, list[float]] = {}

    for row in results:
        for ev in row.get("evals", []) or []:
            key = ev.get("key")
            if not key:
                continue
            score = float(ev.get("score", 0.0))
            metrics.setdefault(key, []).append(score)

    metric_summary: dict[str, dict[str, float]] = {}
    for key, scores in metrics.items():
        total = len(scores)
        avg_score = (sum(scores) / total) if total else 0.0
        pass_threshold = PASS_THRESHOLDS.get(key, 1.0)
        pass_rate = (sum(1 for s in scores if s >= pass_threshold) / total) if total else 0.0
        metric_summary[key] = {
            "avg_score": round(avg_score, 4),
            "pass_rate": round(pass_rate, 4),
            "pass_threshold": pass_threshold,
            "samples": total,
        }

    overall_avg = (
        round(sum(v["avg_score"] for v in metric_summary.values()) / len(metric_summary), 4)
        if metric_summary
        else 0.0
    )

    return {
        "experiment": report.get("experiment"),
        "prompt_version": report.get("prompt_version"),
        "example_count": len(results),
        "overall_avg_score": overall_avg,
        "metrics": metric_summary,
    }


def compare_experiments_data(baseline_report: dict[str, Any], candidate_report: dict[str, Any]) -> dict[str, Any]:
    baseline = summarize_experiment(baseline_report)
    candidate = summarize_experiment(candidate_report)

    all_metric_keys = set(baseline["metrics"].keys()) | set(candidate["metrics"].keys())
    metrics: dict[str, dict[str, float]] = {}
    for key in sorted(all_metric_keys):
        b = baseline["metrics"].get(key, {"avg_score": 0.0, "pass_rate": 0.0})
        c = candidate["metrics"].get(key, {"avg_score": 0.0, "pass_rate": 0.0})
        metrics[key] = {
            "baseline_avg": b["avg_score"],
            "candidate_avg": c["avg_score"],
            "delta": round(c["avg_score"] - b["avg_score"], 4),
            "baseline_pass_rate": b["pass_rate"],
            "candidate_pass_rate": c["pass_rate"],
            "pass_rate_delta": round(c["pass_rate"] - b["pass_rate"], 4),
        }

    overall_delta = round(candidate["overall_avg_score"] - baseline["overall_avg_score"], 4)
    if overall_delta > 0:
        winner = "candidate"
    elif overall_delta < 0:
        winner = "baseline"
    else:
        winner = "tie"

    return {
        "baseline": baseline,
        "candidate": candidate,
        "overall_delta": overall_delta,
        "winner": winner,
        "metrics": metrics,
    }


def save_comparison_report(
    comparison: dict[str, Any], baseline_name: str, candidate_name: str, reports_dir: Path | None = None
) -> Path:
    base = reports_dir or REPORTS_DIR
    base.mkdir(parents=True, exist_ok=True)
    out_path = base / f"compare-{baseline_name}__vs__{candidate_name}.json"
    out_path.write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path
