from __future__ import annotations

from langsmith import Client


def create_feedback_for_run(run_id: str, key: str = "human_quality", score: float = 0.8, comment: str = "Solid draft") -> None:
    client = Client()
    client.create_feedback(run_id=run_id, key=key, score=score, comment=comment)
