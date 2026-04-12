from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.pipeline import generate_ops_reflection_brief

if __name__ == "__main__":
    out = generate_ops_reflection_brief(
        user_input="Summarize a reliability incident and provide an action plan.",
        prompt_version="v1",
    )
    print(out)
