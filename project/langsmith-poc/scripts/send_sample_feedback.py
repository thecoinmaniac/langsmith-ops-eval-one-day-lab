import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.feedback import create_feedback_for_run


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--score", type=float, default=0.8)
    parser.add_argument("--key", default="human_quality")
    parser.add_argument("--comment", default="Useful and aligned with target tone")
    args = parser.parse_args()

    create_feedback_for_run(
        run_id=args.run_id,
        key=args.key,
        score=args.score,
        comment=args.comment,
    )
    print("Feedback submitted")
