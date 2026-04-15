from __future__ import annotations

import re
from typing import Any, Dict, List


THEME_LEXICON: dict[str, list[str]] = {
    "incident-analysis": ["incident", "outage", "degradation", "postmortem", "root cause"],
    "postmortem": ["postmortem", "lesson learned", "retrospective"],
    "incident-response": ["mitigation", "triage", "containment", "escalation", "rollback"],
    "oncall-operations": ["on-call", "pager", "alert", "mttr", "escalation"],
    "service-ownership": ["ownership", "owner", "accountability", "runbook"],
    "database-reliability": ["database", "migration", "lock", "query", "index"],
    "kubernetes-operations": ["kubernetes", "pod", "node", "cluster", "evict"],
    "deployment-safety": ["deploy", "rollback", "canary", "feature flag", "blast radius"],
    "release-management": ["release", "rollout", "change window", "approval", "rollback"],
    "observability": ["monitor", "metric", "slo", "latency", "dashboard"],
    "sre-practices": ["slo", "error budget", "mttr", "runbook", "reliability"],
    "resilience-engineering": ["retry", "backoff", "timeout", "resilience", "fallback"],
    "security-controls": ["security", "guardrail", "rbac", "policy", "least privilege"],
    "infrastructure-security": ["terraform", "iac", "policy-as-code", "compliance", "security"],
    "secret-management": ["secret", "key rotation", "vault", "credential", "token"],
    "risk-management": ["risk", "blast radius", "safeguard", "control", "mitigation"],
    "governance": ["governance", "approval", "policy", "audit", "compliance"],
    "ai-governance": ["ai assistant", "model", "guardrail", "approval", "workflow"],
    "change-management": ["change", "workflow", "approval", "owner", "communication"],
    "continuous-improvement": ["improve", "iteration", "feedback", "measure", "follow-up"],
    "operating-model": ["ownership", "process", "cadence", "policy", "review"],
    "incident-prevention": ["prevention", "recurrence", "action item", "follow-up", "hardening"],
    "performance-reliability": ["latency", "throughput", "timeout", "performance", "availability"],
    "network-reliability": ["dns", "network", "routing", "service discovery", "connectivity"],
    "multi-region-resilience": ["region", "failover", "replication", "resilience", "availability"],
    "stream-processing": ["kafka", "consumer", "partition", "rebalance", "event"],
    "data-consistency": ["stale", "consistency", "cache", "invalidation", "integrity"],
    "platform-operations": ["platform", "automation", "pipeline", "infrastructure", "operations"],
    "finops": ["cost", "spend", "budget", "utilization", "idle"],
    "quality-engineering": ["test", "validation", "quality", "flaky", "regression"],
    "developer-productivity": ["ci", "pipeline", "build", "developer", "throughput"],
    "proactive-operations": ["synthetic", "proactive", "early warning", "monitoring", "prevention"],
    "incident-communications": ["communication", "status update", "stakeholder", "timeline", "impact"],
    "stakeholder-management": ["stakeholder", "customer", "leadership", "expectation", "communication"],
}


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


def semantic_theme_alignment_evaluator(run_output: str, semantic_targets: List[str]) -> Dict[str, Any]:
    """
    Lightweight semantic evaluator using theme-level concept lexicon.
    Scores based on how many target themes are represented in output language.
    """
    text = _normalized(run_output)

    if not semantic_targets:
        return {
            "key": "semantic_theme_alignment",
            "score": 1.0,
            "comment": "no semantic targets specified",
        }

    matched = []
    missing = []
    for theme in semantic_targets:
        terms = THEME_LEXICON.get(theme, [theme])
        if any(_normalized(term) in text for term in terms):
            matched.append(theme)
        else:
            missing.append(theme)

    coverage = len(matched) / len(semantic_targets)
    return {
        "key": "semantic_theme_alignment",
        "score": round(coverage, 3),
        "comment": f"matched={matched}, missing={missing}, coverage={coverage:.2f}",
    }
