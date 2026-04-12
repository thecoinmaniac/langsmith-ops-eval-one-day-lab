from __future__ import annotations

import re
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

    if not required_terms:
        return {
            "key": "must_include",
            "score": 1.0,
            "comment": "no required terms specified",
        }

    present = [t for t in required_terms if _normalized(t) in text]
    missing = [t for t in required_terms if _normalized(t) not in text]
    coverage = len(present) / len(required_terms)

    return {
        "key": "must_include",
        "score": round(coverage, 3),
        "comment": f"present={present}, missing={missing}, coverage={coverage:.2f}",
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


def operational_specificity_evaluator(run_output: str) -> Dict[str, Any]:
    """
    Anti-gaming evaluator focused on practical signal quality.

    Gives 1 point for each present signal (max 4):
    - metric/number evidence
    - explicit causal language
    - concrete action verb
    - risk/guardrail/security language
    """
    text = _normalized(run_output)

    has_metric = bool(re.search(r"\d+(?:\.\d+)?|p\d{2}|mttr|slo", text))
    has_cause = any(tok in text for tok in ["root cause", "caused by", "because", "due to"])
    has_action = any(tok in text for tok in ["implement", "add", "remove", "rollback", "monitor", "alert", "validate", "test"])
    has_risk = any(tok in text for tok in ["risk", "guardrail", "security", "blast radius", "safeguard"])

    total = sum([has_metric, has_cause, has_action, has_risk])
    score = total / 4.0

    return {
        "key": "operational_specificity",
        "score": round(score, 3),
        "comment": (
            f"metric={has_metric}, cause={has_cause}, action={has_action}, "
            f"risk={has_risk}, points={total}/4"
        ),
    }
