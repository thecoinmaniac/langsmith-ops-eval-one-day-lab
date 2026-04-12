from pathlib import Path
import json

from src.langsmith_poc.comparison import summarize_experiment, compare_experiments_data, load_experiment_report


def _sample_report(name: str):
    return {
        "experiment": name,
        "prompt_version": "v1",
        "results": [
            {
                "example_id": "1",
                "evals": [
                    {"key": "format_length", "score": 1.0},
                    {"key": "hashtag_count", "score": 0.0},
                ],
            },
            {
                "example_id": "2",
                "evals": [
                    {"key": "format_length", "score": 0.0},
                    {"key": "hashtag_count", "score": 1.0},
                ],
            },
        ],
    }


def test_summarize_experiment_computes_per_metric_scores():
    report = _sample_report("exp-a")
    summary = summarize_experiment(report)

    assert summary["experiment"] == "exp-a"
    assert summary["example_count"] == 2
    assert summary["metrics"]["format_length"]["avg_score"] == 0.5
    assert summary["metrics"]["format_length"]["pass_rate"] == 0.5
    assert summary["metrics"]["hashtag_count"]["avg_score"] == 0.5


def test_compare_experiments_data_computes_metric_deltas():
    baseline = _sample_report("base")
    candidate = {
        "experiment": "cand",
        "prompt_version": "v2",
        "results": [
            {
                "example_id": "1",
                "evals": [
                    {"key": "format_length", "score": 1.0},
                    {"key": "hashtag_count", "score": 1.0},
                ],
            },
            {
                "example_id": "2",
                "evals": [
                    {"key": "format_length", "score": 1.0},
                    {"key": "hashtag_count", "score": 1.0},
                ],
            },
        ],
    }

    comparison = compare_experiments_data(baseline, candidate)

    assert comparison["winner"] == "candidate"
    assert comparison["metrics"]["format_length"]["delta"] == 0.5
    assert comparison["metrics"]["hashtag_count"]["delta"] == 0.5


def test_load_experiment_report_reads_from_reports_dir(tmp_path: Path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir(parents=True)
    payload = _sample_report("exp-file")
    path = reports_dir / "exp-file.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    loaded = load_experiment_report("exp-file", reports_dir=reports_dir)
    assert loaded["experiment"] == "exp-file"
