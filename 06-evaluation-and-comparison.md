# Evaluation Logic and Interpretation

## Evaluators in this lab
1) format_length
- Purpose: ensure communication is concise but complete.
- Rule: 120-260 words.

2) section_coverage
- Purpose: enforce operational structure.
- Expected sections:
  - What Happened
  - Operational Impact
  - Action Plan
  - Lesson Learned

3) must_include (coverage-based)
- Purpose: ensure scenario-critical language appears.
- Scoring: partial coverage ratio from 0.0 to 1.0.
- Why: avoids brittle all-or-nothing scoring.

4) operational_specificity (anti-gaming)
- Purpose: verify practical engineering substance.
- Signals checked:
  - metric/number evidence
  - causal language (root cause / due to / because)
  - concrete action verbs
  - risk/guardrail/security language

## Integrity guardrail: realistic vs deterministic mode
Default recommended mode:
- `POC_INJECT_REQUIRED_TERMS_IN_PROMPT=false`
- This avoids artificially feeding required keywords into the model.

Optional debug mode:
- `POC_INJECT_REQUIRED_TERMS_IN_PROMPT=true`
- Useful only for deterministic troubleshooting, not for honest benchmark claims.

## How to interpret outcomes
- If `format_length` fails, response may be too thin or verbose.
- If `section_coverage` fails, output is operationally incomplete.
- If `must_include` is low, key concepts are missing.
- If `operational_specificity` is low, output may be generic despite passing structure checks.

## Decision framework
Candidate is promoted only if:
1. Overall score delta is non-negative and quality is stable.
2. `operational_specificity` does not regress materially.
3. Trace inspection confirms outputs are actionable, not template-like.
