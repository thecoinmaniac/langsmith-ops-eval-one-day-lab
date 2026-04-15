from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from langsmith import Client

from .config import get_settings
from .pipeline import generate_ops_reflection_brief
from .evaluators import (
    format_length_evaluator,
    must_include_evaluator,
    section_coverage_evaluator,
    operational_specificity_evaluator,
    semantic_theme_alignment_evaluator,
)


REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "golden_inputs.jsonl"


def _load_source_split_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not DATA_FILE.exists():
        return mapping

    for line in DATA_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        source_id = str(row.get("id", "")).strip()
        split = str(row.get("split", "train")).strip().lower()
        if source_id:
            mapping[source_id] = split if split in {"train", "holdout"} else "train"
    return mapping


def run_experiment(prompt_version: str = "v1", split: str | None = None) -> str:
    settings = get_settings()
    client = Client()

    effective_split = (split or settings.dataset_split or "all").strip().lower()
    if effective_split not in {"all", "train", "holdout"}:
        raise ValueError(f"Invalid split '{effective_split}'. Use all|train|holdout")

    experiment_name = f"{settings.experiment_prefix}-{prompt_version}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    dataset = client.read_dataset(dataset_name=settings.dataset_name)
    examples = list(client.list_examples(dataset_id=dataset.id))

    if effective_split != "all":
        source_split_map = _load_source_split_map()
        filtered = []
        for ex in examples:
            meta = getattr(ex, "metadata", None) or {}
            ex_split = str(meta.get("split", "")).strip().lower()

            # Backward compatibility: older datasets may miss metadata.split
            if not ex_split:
                source_id = str(meta.get("source_id", "")).strip()
                ex_split = source_split_map.get(source_id, "train")

            if ex_split == effective_split:
                filtered.append(ex)
        examples = filtered

    if not examples:
        raise RuntimeError(
            f"No examples found for split='{effective_split}' in dataset '{settings.dataset_name}'. "
            "Run scripts/create_dataset.py with the current JSONL first."
        )

    results: list[dict[str, Any]] = []
    for ex in examples:
        user_input = ex.inputs.get("user_input", "")
        required_terms = ex.outputs.get("must_include", []) if ex.outputs else []
        semantic_targets = ex.outputs.get("semantic_targets", []) if ex.outputs else []

        scenario = user_input
        if settings.inject_required_terms_in_prompt and required_terms:
            scenario = f"{user_input}\n\nRequired terms to include verbatim: {', '.join(required_terms)}"

        output = generate_ops_reflection_brief(user_input=scenario, prompt_version=prompt_version)

        evals = [
            format_length_evaluator(output),
            section_coverage_evaluator(output),
            must_include_evaluator(output, required_terms),
            operational_specificity_evaluator(output),
            semantic_theme_alignment_evaluator(output, semantic_targets),
        ]
        row = {
            "experiment": experiment_name,
            "example_id": str(ex.id),
            "prompt_version": prompt_version,
            "split": effective_split,
            "evals": evals,
            "output_preview": output[:300],
        }
        results.append(row)
        print(row)

    report = {
        "experiment": experiment_name,
        "prompt_version": prompt_version,
        "dataset_name": settings.dataset_name,
        "dataset_split": effective_split,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "results": results,
    }
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{experiment_name}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print({"report_path": str(report_path)})

    return experiment_name
