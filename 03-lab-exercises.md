# Lab Exercises (Detailed)

Prerequisite:
- You completed setup in `02-prerequisites-and-setup.md`.
- You are inside project folder: `project/langsmith-poc` (or your copied project path).

## Exercise 1: Create dataset

Why this matters:
- Dataset is your controlled benchmark.
- Same inputs across versions = fair comparison.

Command:
```bash
python scripts/create_dataset.py
```

Expected output:
- `Dataset ready: <uuid>`

What to verify in LangSmith:
- Dataset appears with expected examples.

## Exercise 2: Baseline run (v1)

Why this matters:
- Baseline is the reference point.

Command:
```bash
python scripts/run_experiment.py --prompt-version v1
```

Capture:
- Experiment name
- Report path
- Which evaluators failed/passed

## Exercise 3: Candidate run (v2)

Why this matters:
- Tests whether prompt changes improve real metrics.

Command:
```bash
python scripts/run_experiment.py --prompt-version v2
```

## Exercise 4: Compare experiments

Why this matters:
- Promotion decisions should be metric-driven.

Command:
```bash
python scripts/compare_experiments.py --baseline <v1_name> --candidate <v2_name>
```

Expected:
- Winner output (`baseline`, `candidate`, `tie`)
- Per-metric deltas
- Comparison JSON report saved

## Exercise 5: Monitor recent runs

Why this matters:
- Confirms operational health (errors, timing, run types).

Command:
```bash
python scripts/monitor_runs.py
```

Verify in UI:
- chain run name present
- model runs linked
- no critical errors
