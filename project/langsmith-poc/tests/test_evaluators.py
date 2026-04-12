from src.langsmith_poc.evaluators import (
    format_length_evaluator,
    must_include_evaluator,
    section_coverage_evaluator,
)


def test_format_length_evaluator_passes_in_range():
    text = "word " * 150
    r = format_length_evaluator(text)
    assert r["score"] == 1.0


def test_section_coverage_evaluator_fails_when_sections_missing():
    text = "This is a short unstructured note without required headings."
    r = section_coverage_evaluator(text)
    assert r["score"] == 0.0


def test_must_include_evaluator_detects_missing_terms():
    text = "We discussed root cause and mitigation only"
    r = must_include_evaluator(text, ["root cause", "mitigation", "lesson learned"])
    assert r["score"] == 0.0
