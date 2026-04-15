# LangSmith Ops Reflection PoC

Goal
- Validate a practical LangSmith evaluation workflow for operations reflection content.

What this PoC covers
- Tracing and run observability
- Dataset creation from golden inputs
- Prompt version experiments (v1/v2)
- Evaluator scoring + comparison report
- Monitoring snapshot and optional feedback hooks

Evaluation integrity principles
- Default mode is realism-first: no keyword injection into prompt input.
- `must_include` uses partial coverage scoring (not all-or-nothing).
- `operational_specificity` checks for evidence quality signals (metrics, cause, action, risk).
- `semantic_theme_alignment` checks concept-level alignment against scenario themes.
- Optional deterministic mode exists only for debugging (`POC_INJECT_REQUIRED_TERMS_IN_PROMPT=true`).

Quick start
1) Python env
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt

2) Env vars
   cp .env.example .env
   # Fill in LANGSMITH_API_KEY and provider credentials
   # Example OpenAI-compatible base URL:
   # OPENAI_BASE_URL=https://opencode.ai/zen/go/v1
   # POC_MODEL=minimax-m2.7

3) Create dataset
   python scripts/create_dataset.py

4) Run experiments
   python scripts/run_experiment.py --prompt-version v1 --split train
   python scripts/run_experiment.py --prompt-version v2 --split train

5) Validate on holdout split
   python scripts/run_experiment.py --prompt-version v1 --split holdout
   python scripts/run_experiment.py --prompt-version v2 --split holdout

6) Compare experiments
   python scripts/compare_experiments.py --baseline <exp_v1_name> --candidate <exp_v2_name>

7) Optional promotion gate (regression policy)
   python scripts/promotion_gate.py --baseline <exp_v1_name> --candidate <exp_v2_name> --max-overall-regression 0.02 --require-no-passrate-regression

8) Monitor runs
   python scripts/monitor_runs.py

Project structure
- src/langsmith_poc/: app code
- scripts/: runnable entry points
- data/: golden dataset seed
- prompts/: prompt versions
- tests/: local unit tests for evaluators/comparison
- reports/: generated experiment and comparison evidence
- docs/architecture-week1.md: Week 1 architecture notes
- docs/architecture-updated.md: current architecture + E2E flow notes
- week1-poc-architecture.html: Week 1 standalone architecture diagram (HTML/SVG)
- e2e-validation-architecture.html: E2E validation architecture diagram
- langsmith-ops-eval-one-day-lab-architecture.html: latest updated architecture diagram

Architecture docs and diagrams
- Updated diagram: `./langsmith-ops-eval-one-day-lab-architecture.html`
- Updated notes: `./docs/architecture-updated.md`
- E2E diagram: `./e2e-validation-architecture.html`
- Week 1 baseline diagram: `./week1-poc-architecture.html`
- Week 1 notes: `./docs/architecture-week1.md`
- Open latest diagram (Linux): `xdg-open ./langsmith-ops-eval-one-day-lab-architecture.html`

Reviewer evidence table (2-minute scan)
| Goal | Command | Evidence to check |
|---|---|---|
| Reproducible environment | `python -m pytest -q` | All tests pass (currently 10/10). |
| Local sanity without API cost | `python scripts/smoke_test.py` | "Local smoke passed" output. |
| Dataset bootstrap | `python scripts/create_dataset.py` | Prints dataset ID and no duplication errors. |
| Train experiment run | `python scripts/run_experiment.py --prompt-version v1 --split train` | Creates `reports/ops-reflections-*.json` with per-example eval rows. |
| Holdout validation | `python scripts/run_experiment.py --prompt-version v2 --split holdout` | Separate holdout-only report (`dataset_split=holdout`). |
| Prompt comparison | `python scripts/compare_experiments.py --baseline <exp1> --candidate <exp2>` | Metric deltas + threshold-aware pass rates. |
| Promotion policy gate | `python scripts/promotion_gate.py --baseline <exp1> --candidate <exp2> --max-overall-regression 0.02 --require-no-passrate-regression` | Exit code 0 = pass, non-zero = blocked promotion. |

Notes for reviewers
- Default dataset is `ops-reflections-golden-v2`.
- Default mode is realism-first (`POC_INJECT_REQUIRED_TERMS_IN_PROMPT=false`).
- Train/holdout split is enforced via `--split` for cleaner promotion decisions.
