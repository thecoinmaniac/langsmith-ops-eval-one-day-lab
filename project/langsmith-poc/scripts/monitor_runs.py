from pprint import pprint
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.monitoring import recent_runs_snapshot

if __name__ == "__main__":
    rows = recent_runs_snapshot(hours=24, limit=50)
    pprint(rows)
