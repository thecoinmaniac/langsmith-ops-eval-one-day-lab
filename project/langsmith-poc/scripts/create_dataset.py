from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.datasets import ensure_dataset

if __name__ == "__main__":
    dataset_id = ensure_dataset()
    print(f"Dataset ready: {dataset_id}")
