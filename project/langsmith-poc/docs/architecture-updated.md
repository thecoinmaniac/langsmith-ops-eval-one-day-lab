# Updated Architecture (langsmith-ops-eval-one-day-lab)

This page documents the updated architecture for the LangSmith Ops Reflection PoC after the latest end-to-end validation run.

## Architecture artifacts

- Updated diagram (HTML/SVG): `../langsmith-ops-eval-one-day-lab-architecture.html`
- Previous E2E diagram: `../e2e-validation-architecture.html`
- Week 1 baseline diagram: `../week1-poc-architecture.html`
- This doc: `docs/architecture-updated.md`

Open the updated diagram from project root:

```bash
xdg-open ./langsmith-ops-eval-one-day-lab-architecture.html
```

## System planes

1) Local development plane
- Script-driven workflow from `scripts/`
- Runtime in `src/langsmith_poc/`:
  - `config.py`
  - `datasets.py`
  - `pipeline.py`
  - `experiments.py`
  - `monitoring.py`
- Local artifacts in `reports/` for reproducible evidence

2) Cloud evaluation plane
- LangSmith dataset API for dataset bootstrap and example management
- LangSmith run/trace store for experiment observability
- LangSmith UI for comparison and monitoring views
- OpenAI-compatible provider path for model inference

## Execution flow (updated)

1. Local gates
- `python -m pytest -q`
- `python scripts/smoke_test.py`

2. Dataset bootstrap
- `python scripts/create_dataset.py`

3. Experiment runs
- Train split: v1 and v2
- Holdout split: v1 and v2

4. Decision steps
- Compare baseline vs candidate (`compare_experiments.py`)
- Apply promotion policy gate (`promotion_gate.py`)
- Inspect health snapshots (`monitor_runs.py`)

## Configuration and controls

- `OPENAI_BASE_URL=https://opencode.ai/zen/go/v1`
- `POC_MODEL=minimax-m2.7`
- Dataset target: `ops-reflections-golden-v2`
- LangSmith project: `poc-langsmith-dev`
- Promotion gate policy (current):
  - max overall regression: `0.02`
  - no pass-rate regression required

## Failure modes and triage path

1. LangSmith auth failure
- Signature: `401 Unauthorized` / `Invalid token`
- Check: `LANGSMITH_API_KEY`

2. Empty split selection
- Signature: no examples for selected split
- Check: `metadata.split` values and source JSONL consistency

3. Provider endpoint/model issues
- Signature: inference errors/timeouts
- Check: base URL root and model configuration

4. Quality drift
- Signature: candidate loses on key metrics or fails gate
- Action: inspect per-metric deltas in compare report, then iterate prompt/evaluator settings

## Current status snapshot

- End-to-end run completed successfully (local + cloud)
- Candidate prompt (v2) outperformed baseline (v1) in the latest comparison run
- Promotion gate passed under current policy
- Reports persisted in `reports/` for traceable review
