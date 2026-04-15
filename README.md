# One-Day Mini Lab: LangSmith Evaluation for Ops Reflections

## Course overview
This one-day mini lab teaches you how to evaluate LLM output with engineering rigor using LangSmith.

Instead of approving prompt changes by intuition, you run controlled experiments, inspect traces, and make decisions from metrics.

The scenario theme is operational reflections (incident communication, reliability updates, and action plans), aligned with cloud/DevOps/SRE workflows.

## Learning objectives
By the end of this lab, you should be able to:
1. Build a reusable LangSmith dataset from domain scenarios.
2. Run baseline and candidate prompt experiments reproducibly.
3. Inspect traces to identify quality and failure patterns.
4. Compare prompt versions with metric deltas and pass-rate behavior.
5. Make a promotion/hold decision based on evidence.

## LangSmith features covered
1. Tracing and observability (chain + model runs)
2. Dataset management (create/reuse examples)
3. Versioned experiments (v1 vs v2)
4. Evaluator scoring per example
5. Comparison reporting + monitoring snapshots

## Target audience
- Cloud architects
- DevOps/SRE engineers
- AI/LLMOps practitioners
- Platform teams introducing LLM quality gates

## Repository layout
- Root: learning modules and runbooks
- `project/langsmith-poc/`: full runnable project code for the lab

## One-day agenda
- Block 1: setup + credentials + dataset
- Block 2: baseline experiment (v1)
- Block 3: candidate experiment (v2)
- Block 4: comparison + trace review + decision memo

## Quick start
1) Clone the repo
```bash
git clone <your_repo_url> /home/ubuntu/langsmith-ops-eval-one-day-lab
cd /home/ubuntu/langsmith-ops-eval-one-day-lab
```

2) Move into project code
```bash
cd project/langsmith-poc
```

3) Follow docs in order
- Setup: `../../02-prerequisites-and-setup.md`
- Exercises: `../../03-lab-exercises.md`
- Runbook: `../../04-operations-runbook.md`

## Provider note
This project uses OpenAI-compatible APIs.
You can use Opencode, OpenRouter, or another compatible endpoint.

In this lab version, Opencode Go is shown as a cost-effective example for iterative experiments.

## Path convention
All docs use generic Linux paths:
- Lab root: `/home/ubuntu/langsmith-ops-eval-one-day-lab`
- Project root: `/home/ubuntu/langsmith-ops-eval-one-day-lab/project/langsmith-poc`

Adjust as needed for your machine.

## Reviewer fast path
For a quick technical review:
1. Open `project/langsmith-poc/README.md` (Reviewer evidence table)
2. Run:
   ```bash
   cd project/langsmith-poc
   python -m pytest -q
   python scripts/smoke_test.py
   ```
3. Inspect one holdout run + comparison + promotion gate result

## vNext credibility sprint (implemented)
- Dataset expanded to 24 examples
- Added semantic theme alignment evaluator
- Added GitHub Actions CI (tests + smoke)

## Evaluation protocol update
- Train split for prompt iteration
- Holdout split for promotion checks
