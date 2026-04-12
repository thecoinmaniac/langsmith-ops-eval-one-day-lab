import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.comparison import (
    compare_experiments_data,
    load_experiment_report,
    save_comparison_report,
)


def _fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, help="Baseline experiment name")
    parser.add_argument("--candidate", required=True, help="Candidate experiment name")
    args = parser.parse_args()

    baseline_report = load_experiment_report(args.baseline)
    candidate_report = load_experiment_report(args.candidate)
    comparison = compare_experiments_data(baseline_report, candidate_report)

    print("Experiment comparison")
    print(f"Baseline : {comparison['baseline']['experiment']} (avg={comparison['baseline']['overall_avg_score']:.3f})")
    print(f"Candidate: {comparison['candidate']['experiment']} (avg={comparison['candidate']['overall_avg_score']:.3f})")
    print(f"Winner   : {comparison['winner']} (delta={comparison['overall_delta']:+.3f})")
    print("\nPer-metric deltas:")

    for key, row in comparison["metrics"].items():
        print(
            "- "
            f"{key}: avg {row['baseline_avg']:.3f} -> {row['candidate_avg']:.3f} "
            f"(delta {row['delta']:+.3f}), pass {_fmt_pct(row['baseline_pass_rate'])} -> {_fmt_pct(row['candidate_pass_rate'])} "
            f"(delta {_fmt_pct(row['pass_rate_delta'])})"
        )

    out_path = save_comparison_report(comparison, args.baseline, args.candidate)
    print(f"\nSaved JSON report: {out_path}")


if __name__ == "__main__":
    main()
