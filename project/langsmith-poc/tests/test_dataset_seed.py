import json
from pathlib import Path


def test_golden_inputs_size_and_splits():
    data_path = Path(__file__).resolve().parents[1] / "data" / "golden_inputs.jsonl"
    rows = [json.loads(line) for line in data_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(rows) >= 20
    split_counts = {"train": 0, "holdout": 0}
    for row in rows:
        split = row.get("split")
        assert split in {"train", "holdout"}
        split_counts[split] += 1

    assert split_counts["train"] >= 14
    assert split_counts["holdout"] >= 4


def test_every_example_has_semantic_targets():
    data_path = Path(__file__).resolve().parents[1] / "data" / "golden_inputs.jsonl"
    rows = [json.loads(line) for line in data_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    for row in rows:
        assert isinstance(row.get("semantic_targets"), list)
        assert len(row["semantic_targets"]) >= 2
