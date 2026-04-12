from src.langsmith_poc.evaluators import (
    format_length_evaluator,
    must_include_evaluator,
    section_coverage_evaluator,
    operational_specificity_evaluator,
)


def test_format_length_evaluator_passes_in_range():
    text = "word " * 150
    r = format_length_evaluator(text)
    assert r["score"] == 1.0


def test_section_coverage_evaluator_fails_when_sections_missing():
    text = "This is a short unstructured note without required headings."
    r = section_coverage_evaluator(text)
    assert r["score"] == 0.0


def test_must_include_evaluator_returns_partial_coverage_score():
    text = "We discussed root cause and mitigation only"
    r = must_include_evaluator(text, ["root cause", "mitigation", "lesson learned"])
    assert r["score"] == 0.667


def test_operational_specificity_evaluator_scores_multiple_signals():
    text = (
        "Root cause was lock contention due to migration. "
        "We will implement rollback guardrails and monitor p99 latency at 200ms."
    )
    r = operational_specificity_evaluator(text)
    assert r["score"] >= 0.75
