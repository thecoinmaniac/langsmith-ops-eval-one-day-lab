# Prerequisites and Setup (Detailed)

This guide takes a learner from zero to a runnable, reviewable environment.

## 1) What you are setting up (and why)
You are preparing three layers:
1. Runtime layer: Python + dependencies (so scripts run consistently)
2. Observability layer: LangSmith account + API key (so traces/evals are inspectable)
3. Inference layer: OpenAI-compatible model endpoint (so experiments can execute)

Without these three layers, you cannot produce credible experiment evidence.

## 2) System dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl
python3 --version
git --version
```

Recommended Python version: 3.11.

## 3) Clone the mini-lab repository
```bash
git clone <your_repo_url> /home/ubuntu/langsmith-ops-eval-one-day-lab
cd /home/ubuntu/langsmith-ops-eval-one-day-lab
```

What should exist now:
- Course docs at repo root
- Runnable project code under `project/langsmith-poc`

## 4) Enter the project code folder
```bash
cd /home/ubuntu/langsmith-ops-eval-one-day-lab/project/langsmith-poc
pwd
```

Expected path:
`/home/ubuntu/langsmith-ops-eval-one-day-lab/project/langsmith-poc`

## 5) Create and activate virtual environment
Why:
- avoids system Python conflicts (PEP 668 issues)
- makes the lab reproducible across machines

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Validate:
```bash
which python
python --version
pip --version
```

Expected:
- `which python` points to `.venv/bin/python`

## 6) Create LangSmith account and API key
Why:
- LangSmith is your evidence system (traces, runs, evaluator outputs, metadata)

Steps:
1. Open https://smith.langchain.com/
2. Sign up or log in
3. Create/select a workspace and project name
4. Generate API key from settings
5. Store key in `.env` only (never commit secrets)

## 7) Choose your OpenAI-compatible provider
Supported examples:
- Opencode
- OpenRouter
- Other OpenAI-compatible gateways

Course recommendation for low-cost iteration:
- Opencode Go

Important provider rules:
- `OPENAI_BASE_URL` must be the API base URL (not a route like `/messages`)
- `POC_MODEL` must be exactly what provider supports

## 8) Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and set:

LangSmith:
- `LANGSMITH_TRACING=true`
- `LANGSMITH_ENDPOINT=https://api.smith.langchain.com`
- `LANGSMITH_API_KEY=<your_langsmith_api_key>`
- `LANGSMITH_PROJECT=<your_project_name>`

Provider:
- `OPENAI_BASE_URL=<provider_base_url>`
- `OPENAI_API_KEY=<provider_api_key>` or provider alias key (example: `OPENCODE_API_KEY`)
- `POC_MODEL=<provider_model_name>`

Project defaults:
- `POC_USE_CASE=ops_reflection`
- `POC_DATASET_NAME=ops-reflections-golden-v1`
- `POC_EXPERIMENT_PREFIX=ops-reflections`
- `POC_INJECT_REQUIRED_TERMS_IN_PROMPT=false`

Opencode Go example:
- `OPENAI_BASE_URL=https://opencode.ai/zen/go/v1`
- `POC_MODEL=minimax-m2.7`

## 9) Run setup verification checks
```bash
python scripts/create_dataset.py
python scripts/run_experiment.py --prompt-version v1 --split train
python scripts/monitor_runs.py
```

Expected signals:
- dataset UUID printed
- experiment name printed
- monitor command lists recent runs without auth/model errors

## 10) What success looks like in LangSmith
- Dataset is visible with seeded examples
- At least one chain run is visible (`generate_ops_reflection_brief`)
- Evaluator feedback appears in run metadata
- No repeated authentication failures

## 11) Common setup failures and fixes
1. Wrong base URL shape
- Symptom: provider rejects requests despite valid key
- Fix: set `OPENAI_BASE_URL` to API base root only

2. Wrong model ID
- Symptom: 400/401 model-not-supported
- Fix: use exact provider model string

3. Missing venv activation
- Symptom: missing dependencies or interpreter mismatch
- Fix: `source .venv/bin/activate` before running scripts

4. LangSmith key/project mismatch
- Symptom: traces not visible in expected project
- Fix: verify `LANGSMITH_API_KEY` + `LANGSMITH_PROJECT` in `.env`

5. Secret leakage risk
- Symptom: `.env` staged by git
- Fix: run `git status` and remove `.env` from staging immediately
