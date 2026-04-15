from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from langsmith_poc.pipeline import load_prompt, generate_ops_reflection_brief
from langsmith_poc.evaluators import (
    format_length_evaluator,
    section_coverage_evaluator,
    must_include_evaluator,
    operational_specificity_evaluator,
    semantic_theme_alignment_evaluator,
)


def local_smoke() -> None:
    p1 = load_prompt("v1")
    p2 = load_prompt("v2")
    assert "What Happened:" in p1
    assert "Operational Impact:" in p2

    sample = (
        "What Happened: API latency rose to p99 1.2s due to lock contention. "
        "Operational Impact: checkout errors increased. "
        "Action Plan: implement lock-time alerts and rollback strategy. "
        "Lesson Learned: define guardrails and update runbook."
    )
    evals = [
        format_length_evaluator(sample, min_words=20, max_words=260),
        section_coverage_evaluator(sample),
        must_include_evaluator(sample, ["lock", "runbook", "guardrails"]),
        operational_specificity_evaluator(sample),
        semantic_theme_alignment_evaluator(sample, ["incident-analysis", "observability"]),
    ]
    keys = {e["key"] for e in evals}
    required_keys = {
        "format_length",
        "section_coverage",
        "must_include",
        "operational_specificity",
        "semantic_theme_alignment",
    }
    assert required_keys.issubset(keys)
    print("Local smoke passed: prompts + evaluators OK")


def live_smoke() -> None:
    out = generate_ops_reflection_brief(
        user_input="Summarize a reliability incident and provide an action plan.",
        prompt_version="v1",
    )
    assert isinstance(out, str) and len(out) > 50
    print("Live smoke passed: generation API reachable")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Run live model-generation smoke test")
    args = parser.parse_args()

    local_smoke()
    if args.live:
        live_smoke()
