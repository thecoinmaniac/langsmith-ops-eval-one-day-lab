from __future__ import annotations

from typing import Any, Dict, List


def _normalized(text: str) -> str:
    return (text or "").lower().strip()


def format_length_evaluator(run_output: str, min_words: int = 120, max_words: int = 260) -> Dict[str, Any]:
    words = len((run_output or "").split())
    passed = min_words <= words <= max_words
    return {
        "key": "format_length",
        "score": 1.0 if passed else 0.0,
        "comment": f"word_count={words}, expected={min_words}-{max_words}",
    }


def must_include_evaluator(run_output: str, required_terms: List[str]) -> Dict[str, Any]:
    text = _normalized(run_output)
    missing = [t for t in required_terms if _normalized(t) not in text]
    passed = len(missing) == 0
    return {
        "key": "must_include",
        "score": 1.0 if passed else 0.0,
        "comment": "all required terms found" if passed else f"missing={missing}",
    }


def section_coverage_evaluator(
    run_output: str,
    required_sections: List[str] | None = None,
) -> Dict[str, Any]:
    required_sections = required_sections or [
        "what happened",
        "operational impact",
        "action plan",
        "lesson learned",
    ]
    text = _normalized(run_output)
    present = [s for s in required_sections if s in text]
    passed = len(present) >= 3
    return {
        "key": "section_coverage",
        "score": 1.0 if passed else 0.0,
        "comment": f"present={present}, required={required_sections}, threshold=3",
    }
