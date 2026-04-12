# Prerequisites and Setup (Detailed)

This guide takes a new learner from zero to a runnable lab environment.

## 1) What you are setting up
You are preparing three things:
1. Runtime environment (Python + dependencies)
2. Observability backend (LangSmith account + API key)
3. Inference provider (OpenAI-compatible API endpoint)

Once these are configured, you can run repeatable experiments and inspect traces in LangSmith.

## 2) Install system dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl
python3 --version
git --version
```

Recommended Python version: 3.11.

## 3) Clone this lab repository
```bash
git clone <your_repo_url> /home/ubuntu/langsmith-ops-eval-one-day-lab
cd /home/ubuntu/langsmith-ops-eval-one-day-lab
```

## 4) Enter the included project code
This repo contains full runnable code in:
`project/langsmith-poc`

```bash
cd project/langsmith-poc
pwd
```

Optional (canonical course path):
```bash
mkdir -p /home/ubuntu/pocs
cp -r project/langsmith-poc /home/ubuntu/pocs/langsmith-poc
cd /home/ubuntu/pocs/langsmith-poc
```

## 5) Create and activate virtual environment
Why this matters:
- avoids package conflicts with system Python
- keeps your lab reproducible

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

## 6) Create LangSmith account + API key
Why this matters:
- LangSmith stores traces, datasets, run metadata, and evaluation context.

Steps:
1. Open: https://smith.langchain.com/
2. Sign up or log in
3. Create/select a project workspace
4. Generate an API key from settings
5. Copy key securely (do not commit to git)

## 7) Choose OpenAI-compatible provider
This project supports any OpenAI-compatible endpoint, such as:
- Opencode
- OpenRouter
- self-hosted compatible gateways

Course recommendation:
- Use Opencode Go for cost-efficient iterative runs.

## 8) Configure environment variables
```bash
cp .env.example .env
```

Edit `.env`:

LangSmith:
- `LANGSMITH_TRACING=true`
- `LANGSMITH_ENDPOINT=https://api.smith.langchain.com`
- `LANGSMITH_API_KEY=<your_langsmith_key>`
- `LANGSMITH_PROJECT=<your_project_name>`

Provider:
- `OPENAI_BASE_URL=<provider_base_url>`
- `OPENAI_API_KEY=<provider_api_key>` OR provider alias key (for example `OPENCODE_API_KEY`)
- `POC_MODEL=<provider_supported_model>`

Project settings:
- `POC_USE_CASE=ops_reflection`
- `POC_DATASET_NAME=ops-reflections-golden-v1`
- `POC_EXPERIMENT_PREFIX=ops-reflections`

Example values (Opencode Go):
- `OPENAI_BASE_URL=https://opencode.ai/zen/go/v1`
- `POC_MODEL=minimax-m2.7`

## 9) Run smoke checks
```bash
python scripts/create_dataset.py
python scripts/run_experiment.py --prompt-version v1
python scripts/monitor_runs.py
```

Expected signals:
- Dataset UUID printed
- Experiment name printed
- No authentication/model errors

## 10) Common setup failures and fixes
1. Wrong base URL shape
- Problem: using endpoint routes like `/messages` instead of API base path.
- Fix: set `OPENAI_BASE_URL` to provider base URL only.

2. Wrong model ID
- Problem: provider rejects model name.
- Fix: use exact provider model string.

3. Missing virtualenv activation
- Problem: missing packages or version mismatch.
- Fix: `source .venv/bin/activate` before running scripts.

4. LangSmith key/project issues
- Problem: traces not visible.
- Fix: verify `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT` in `.env`.
