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
   python scripts/run_experiment.py --prompt-version v1
   python scripts/run_experiment.py --prompt-version v2

5) Compare experiments
   python scripts/compare_experiments.py --baseline <exp_v1_name> --candidate <exp_v2_name>

6) Monitor runs
   python scripts/monitor_runs.py

Project structure
- src/langsmith_poc/: app code
- scripts/: runnable entry points
- data/: golden dataset seed
- prompts/: prompt versions
- tests/: local unit tests for evaluators/comparison
