from __future__ import annotations

from datetime import datetime, timedelta, timezone
from langsmith import Client
from .config import get_settings


def recent_runs_snapshot(hours: int = 24, limit: int = 50) -> list[dict]:
    settings = get_settings()
    client = Client()
    start = datetime.now(timezone.utc) - timedelta(hours=hours)

    out = []
    for run in client.list_runs(project_name=settings.langsmith_project, start_time=start, limit=limit):
        out.append({
            "id": str(run.id),
            "name": run.name,
            "run_type": run.run_type,
            "start_time": str(run.start_time),
            "end_time": str(run.end_time),
            "error": run.error,
        })
    return out
