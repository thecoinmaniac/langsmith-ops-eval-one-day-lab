# GitHub/GitLab Publish Checklist

## 1) Commit locally
```bash
cd /home/ubuntu/langsmith-ops-eval-one-day-lab
git init
git branch -m main
git config --global user.name "<your_name>"
git config --global user.email "<your_email>"
git add .
git status --short
git commit -m "Add one-day LangSmith ops-eval mini lab"
```

## 2) Pre-push safety checks
```bash
# confirm no secrets or local runtime artifacts are tracked
git status --short
```

Checklist:
- `.env` is NOT tracked
- `.venv/` is NOT tracked
- `__pycache__/` and `*.pyc` are NOT tracked
- `reports/` is NOT tracked

## 3) Push to remote
```bash
git remote add origin <your_repo_url>
git push -u origin main
```

## 4) Post-push validation
- README renders correctly
- Mermaid diagram renders correctly
- `project/langsmith-poc` folder is included
- setup guide works on a fresh machine
- reviewer can run `python -m pytest -q` and `python scripts/smoke_test.py`
