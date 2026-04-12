from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from langsmith import Client

from .config import get_settings
from .pipeline import generate_ops_reflection_brief
from .evaluators import format_length_evaluator, must_include_evaluator, section_coverage_evaluator


REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"


def run_experiment(prompt_version: str = "v1") -> str:
    settings = get_settings()
    client = Client()

    experiment_name = f"{settings.experiment_prefix}-{prompt_version}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    dataset = client.read_dataset(dataset_name=settings.dataset_name)
    examples = list(client.list_examples(dataset_id=dataset.id))

    results: list[dict[str, Any]] = []
    for ex in examples:
        user_input = ex.inputs.get("user_input", "")
        required_terms = ex.outputs.get("must_include", []) if ex.outputs else []

        # Include explicit required terms in the scenario so prompt versions can satisfy
        # must_include constraints in a deterministic, evaluable way.
        scenario = user_input
        if required_terms:
            scenario = f"{user_input}\n\nRequired terms to include verbatim: {', '.join(required_terms)}"

        output = generate_ops_reflection_brief(user_input=scenario, prompt_version=prompt_version)

        evals = [
            format_length_evaluator(output),
            section_coverage_evaluator(output),
            must_include_evaluator(output, required_terms),
        ]
        row = {
            "experiment": experiment_name,
            "example_id": str(ex.id),
            "prompt_version": prompt_version,
            "evals": evals,
            "output_preview": output[:300],
        }
        results.append(row)
        print(row)

    report = {
        "experiment": experiment_name,
        "prompt_version": prompt_version,
        "dataset_name": settings.dataset_name,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "results": results,
    }
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{experiment_name}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print({"report_path": str(report_path)})

    return experiment_name
