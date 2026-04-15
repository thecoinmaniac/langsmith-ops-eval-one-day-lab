# Week 1 PoC Architecture

This document captures the architecture used in the Week 1 LangSmith Ops Reflection PoC.

## Diagram files

- Interactive architecture diagram (HTML/SVG): `../week1-poc-architecture.html`
- This architecture note: `docs/architecture-week1.md`

Open the diagram locally (from project root):

```bash
xdg-open ./week1-poc-architecture.html
```

## Architecture overview

The PoC is split into two planes:

1. Local execution plane (project workspace)
   - Operator runs Python scripts from `scripts/`
   - Runtime logic in `src/langsmith_poc/`:
     - `pipeline.py` for prompt loading + LLM invocation
     - `datasets.py` for dataset bootstrap
     - `experiments.py` for eval loop
     - `monitoring.py` for recent run snapshots
   - Local artifacts:
     - Inputs: `data/golden_inputs.jsonl`
     - Prompt versions: `prompts/ops_brief_v1.txt`, `prompts/ops_brief_v2.txt`
     - Reports: `reports/ops-reflections-*.json`

2. Cloud evaluation plane
   - LangSmith API for dataset/run/trace operations
   - LangSmith dataset: `ops-reflections-golden-v2`
   - LangSmith project: `poc-langsmith-dev`
   - LangSmith UI used for run inspection and experiment comparisons
   - OpenAI-compatible model provider endpoint:
     - `OPENAI_BASE_URL=https://opencode.ai/zen/go/v1`
     - Model configured as `minimax-m2.7`

## Main flow

1. `scripts/create_dataset.py`
   - Seeds or updates LangSmith dataset using JSONL source.
2. `scripts/run_experiment.py --prompt-version v1|v2 --split train|holdout`
   - Generates outputs via ChatOpenAI-compatible endpoint.
   - Scores each row with evaluators:
     - format length
     - section coverage
     - must include (partial coverage)
     - operational specificity
     - semantic theme alignment
3. `scripts/compare_experiments.py --baseline ... --candidate ...`
   - Computes metric deltas and pass-rate deltas.
4. `scripts/promotion_gate.py ...`
   - Applies regression policy thresholds.
5. `scripts/monitor_runs.py`
   - Captures recent run health snapshot from LangSmith.

## Failure modes and debug path

1. Auth failure (`401 Unauthorized` / `Invalid token`)
   - Symptom: dataset/experiment API calls fail.
   - Check: `LANGSMITH_API_KEY` validity and scope.
2. Split filtering returns no examples
   - Symptom: runtime error for missing split examples.
   - Check: `metadata.split` values in dataset examples and source JSONL.
3. Provider endpoint issues
   - Symptom: LLM invocation errors or timeouts.
   - Check: base URL root correctness and provider API key.
4. Before remote calls
   - Run local confidence checks first:
     - `python -m pytest -q`
     - `python scripts/smoke_test.py`

## Suggested operator routine

- Always validate local tests/smoke before cloud calls.
- Run train split first for quick signal.
- Use holdout split before making promotion decisions.
- Store comparison output and promotion decision with experiment names.
