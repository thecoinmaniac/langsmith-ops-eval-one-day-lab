# Lab Exercises (Detailed)

Prerequisites:
- Setup completed from `02-prerequisites-and-setup.md`
- You are inside project folder:
  `/home/ubuntu/langsmith-ops-eval-one-day-lab/project/langsmith-poc`

Core principle for this lab:
- Keep inputs controlled
- Change one variable at a time (prompt version)
- Compare with objective metrics, not intuition

## Exercise 1: Create/reuse dataset

Why this matters:
- Dataset is your benchmark contract.
- Same dataset across experiments = fair comparison.

Command:
```bash
python scripts/create_dataset.py
```

Expected output:
- `Dataset ready: <uuid>`

Verify in LangSmith:
- Dataset exists and contains expected examples.

## Exercise 2: Run baseline (v1) on train split

Why this matters:
- Baseline is your reference before introducing change.

Command:
```bash
python scripts/run_experiment.py --prompt-version v1 --split train
```

Capture:
- Experiment name
- Report path in `reports/`
- Pass/fail behavior by evaluator

## Exercise 3: Run candidate (v2) on train split

Why this matters:
- Tests whether prompt edits improve metrics under same conditions.

Command:
```bash
python scripts/run_experiment.py --prompt-version v2 --split train
```

Capture:
- Candidate experiment name
- New report path
- Differences from baseline

## Exercise 4: Compare train split experiments

Why this matters:
- Turns experiment output into decision evidence.

Command:
```bash
python scripts/compare_experiments.py --baseline <train_v1_name> --candidate <train_v2_name>
```

Expected:
- Winner summary (`baseline`, `candidate`, or `tie`)
- Per-metric average deltas
- Pass-rate deltas
- Comparison JSON artifact saved to `reports/`

## Exercise 5: Validate both prompts on holdout split

Why this matters:
- Holdout checks reduce overfitting to your training examples.

Commands:
```bash
python scripts/run_experiment.py --prompt-version v1 --split holdout
python scripts/run_experiment.py --prompt-version v2 --split holdout
python scripts/compare_experiments.py --baseline <holdout_v1_name> --candidate <holdout_v2_name>
```

Interpretation rule:
- A candidate that only wins on train but regresses on holdout should be held for further iteration.

## Exercise 6: Apply promotion gate policy

Why this matters:
- Converts comparison into an enforceable release decision.

Command:
```bash
python scripts/promotion_gate.py --baseline <holdout_v1_name> --candidate <holdout_v2_name> --max-overall-regression 0.02 --require-no-passrate-regression
```

Expected:
- Exit code 0: candidate allowed
- Non-zero exit code: promotion blocked

## Exercise 7: Monitor run health

Why this matters:
- Confirms system reliability and catches hidden runtime issues.

Command:
```bash
python scripts/monitor_runs.py
```

Verify:
- chain + model runs are visible
- no critical errors in target runs
- timing looks reasonable for your provider

## Exercise 8: Write a short decision memo

Template:
- Baseline experiment: `<name>`
- Candidate experiment: `<name>`
- Train result: `<winner + notable deltas>`
- Holdout result: `<winner + notable deltas>`
- Promotion gate result: `<pass/block>`
- Final decision: `<promote | hold | iterate>`
- Next prompt change hypothesis: `<1 concrete idea>`
