import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.experiments import run_experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-version", default="v1", choices=["v1", "v2"])
    parser.add_argument("--split", default="all", choices=["all", "train", "holdout"], help="Dataset split")
    args = parser.parse_args()
    exp_name = run_experiment(prompt_version=args.prompt_version, split=args.split)
    print(f"Experiment completed: {exp_name}")
