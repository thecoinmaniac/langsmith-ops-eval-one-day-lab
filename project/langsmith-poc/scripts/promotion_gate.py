import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.comparison import load_experiment_report, compare_experiments_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail build if candidate regresses beyond policy")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--max-overall-regression", type=float, default=0.02)
    parser.add_argument("--require-no-passrate-regression", action="store_true")
    args = parser.parse_args()

    baseline_report = load_experiment_report(args.baseline)
    candidate_report = load_experiment_report(args.candidate)
    comparison = compare_experiments_data(baseline_report, candidate_report)

    overall_delta = comparison["overall_delta"]
    failed_reasons: list[str] = []

    if overall_delta < -abs(args.max_overall_regression):
        failed_reasons.append(
            f"overall delta {overall_delta:+.3f} below allowed -{abs(args.max_overall_regression):.3f}"
        )

    if args.require_no_passrate_regression:
        for key, row in comparison["metrics"].items():
            if row["pass_rate_delta"] < 0:
                failed_reasons.append(f"pass-rate regression in {key}: {row['pass_rate_delta']:+.3f}")

    print(f"Gate check: winner={comparison['winner']} overall_delta={overall_delta:+.3f}")

    if failed_reasons:
        print("Promotion gate FAILED:")
        for reason in failed_reasons:
            print(f"- {reason}")
        raise SystemExit(1)

    print("Promotion gate PASSED")


if __name__ == "__main__":
    main()
