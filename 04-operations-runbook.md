# One-Day Operations Runbook

## Working directories
- Lab root: `/home/ubuntu/langsmith-ops-eval-one-day-lab`
- Project root: `/home/ubuntu/pocs/langsmith-poc`

## Start a session
```bash
cd /home/ubuntu/pocs/langsmith-poc
source .venv/bin/activate
```

## Execute full workflow
```bash
python scripts/create_dataset.py
python scripts/run_experiment.py --prompt-version v1
python scripts/run_experiment.py --prompt-version v2
python scripts/compare_experiments.py --baseline <v1_name> --candidate <v2_name>
python scripts/monitor_runs.py
```

## Operational expectations
1) Dataset step
- prints dataset UUID
- dataset visible in LangSmith UI

2) Experiment steps
- each run prints experiment name
- each run writes local report JSON

3) Comparison step
- prints winner/tie and per-metric deltas
- writes compare JSON under `reports/`

4) Monitoring step
- lists recent runs and error status
- successful runs should show null/empty error fields

## Decision policy
Promote candidate only if metrics and trace quality are both acceptable.
If uncertain, keep baseline and iterate on prompt + evaluator design.
