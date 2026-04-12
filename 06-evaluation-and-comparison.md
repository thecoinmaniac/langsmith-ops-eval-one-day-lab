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

3) must_include
- Purpose: ensure scenario-critical language appears.
- Example terms: root cause, mitigation, guardrails, security.

## Why these evaluators were selected
They mimic real technical communication constraints:
- structure (section coverage)
- precision (must_include)
- readability (format length)

## How to interpret outcomes
- If `format_length` fails, content may be too thin or too verbose.
- If `section_coverage` fails, content is operationally incomplete.
- If `must_include` fails, key risk/ownership concepts are missing.

## Decision framework
Candidate is promoted only if:
1. Overall score delta is non-negative and quality is stable.
2. Critical metrics do not regress.
3. Trace inspection confirms outputs are actionable, not generic.
