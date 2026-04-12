# One-Day Course Map

## Day goal
Build and validate a repeatable LangSmith evaluation workflow for operations-focused LLM content.

## Success criteria
By the end of the day, you should have:
1. A reusable dataset in LangSmith.
2. Two completed experiments (v1 baseline, v2 candidate).
3. A comparison report with clear metric deltas.
4. A documented decision: promote candidate, keep baseline, or iterate further.

## Schedule
### Hour 1 — Foundation
- Understand the use case and evaluation strategy.
- Validate Python environment and credentials.
- Create/reuse dataset from golden inputs.

### Hour 2 — Baseline measurement
- Run experiment v1.
- Capture metric outputs and first observations.

### Hour 3 — Candidate measurement
- Run experiment v2 under same dataset conditions.
- Record differences and anomalies.

### Hour 4 — Analysis and decision
- Run comparison script.
- Inspect LangSmith traces and run health.
- Write a short decision memo with next actions.

## Suggested output format for decision memo
- Baseline experiment name
- Candidate experiment name
- Winner/tie
- Metric delta summary
- Trace quality notes
- Final decision and follow-up plan
