from __future__ import annotations

import json
from pathlib import Path
from langsmith import Client

from .config import get_settings


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "golden_inputs.jsonl"


def load_examples() -> list[dict]:
    rows = []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def ensure_dataset() -> str:
    settings = get_settings()
    client = Client()

    dataset_name = settings.dataset_name
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
    except Exception:
        dataset = client.create_dataset(dataset_name=dataset_name, description="LangSmith PoC golden dataset")

    existing_source_ids = set()
    for e in client.list_examples(dataset_id=dataset.id):
        meta = getattr(e, "metadata", None) or {}
        sid = meta.get("source_id")
        if sid:
            existing_source_ids.add(sid)

    rows = load_examples()
    for row in rows:
        # de-dup by metadata.source_id when possible
        source_id = row.get("id")
        if source_id and source_id in existing_source_ids:
            continue
        client.create_example(
            dataset_id=dataset.id,
            inputs={"user_input": row["input"], "expected_style": row.get("expected_style", "operator-first")},
            outputs={"must_include": row.get("must_include", [])},
            metadata={"source_id": source_id, "use_case": settings.use_case},
        )
    return str(dataset.id)
