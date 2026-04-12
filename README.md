# One-Day Mini Lab: LangSmith Evaluation for Ops Reflections

## Course overview
This one-day mini lab teaches you how to evaluate LLM output with engineering rigor using LangSmith.

Instead of approving prompt changes by intuition, you will run controlled experiments and make decisions using trace data + evaluator metrics.

The scenario theme is operational reflections (incident communication, reliability updates, and action plans), which maps well to cloud/DevOps/SRE workflows.

## Learning objectives
By the end of this lab, you should be able to:
1. Build a reusable LangSmith dataset from domain scenarios.
2. Run baseline and candidate prompt experiments reproducibly.
3. Inspect traces to identify quality and failure patterns.
4. Compare prompt versions with metric deltas and pass-rate changes.
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

## What this repository contains
- Course docs in root folder
- Full runnable starter project in `project/langsmith-poc/`

## One-day agenda
- Block 1: setup + credentials + dataset
- Block 2: baseline experiment (v1)
- Block 3: candidate experiment (v2)
- Block 4: comparison + trace review + decision memo

## Quick start for learners
1) Clone the repo
```bash
git clone <your_repo_url> /home/ubuntu/langsmith-ops-eval-one-day-lab
cd /home/ubuntu/langsmith-ops-eval-one-day-lab
```

2) Move into starter project code
```bash
cd project/langsmith-poc
```

3) Follow setup and exercise guides
- Setup: `../../02-prerequisites-and-setup.md`
- Exercises: `../../03-lab-exercises.md`
- Runbook: `../../04-operations-runbook.md`

## Model provider note
This project uses OpenAI-compatible APIs.
You can use Opencode, OpenRouter, or any compatible endpoint.

In this course version, Opencode Go is used because it is cost-effective for rapid experiment iteration.

## Path convention used in this course
All docs use generic Linux paths:
- Lab root: `/home/ubuntu/langsmith-ops-eval-one-day-lab`
- Project root: `/home/ubuntu/pocs/langsmith-poc`

Adjust paths as needed for your local machine.
