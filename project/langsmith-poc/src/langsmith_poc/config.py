from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "poc-langsmith-dev")
    dataset_name: str = os.getenv("POC_DATASET_NAME", "ops-reflections-golden-v2")
    experiment_prefix: str = os.getenv("POC_EXPERIMENT_PREFIX", "ops-reflections")
    model_name: str = os.getenv("POC_MODEL", "gpt-4o-mini")
    use_case: str = os.getenv("POC_USE_CASE", "ops_reflection")

    # Optional split filter for experiments: all|train|holdout
    dataset_split: str = os.getenv("POC_DATASET_SPLIT", "all").strip().lower()

    # OpenAI-compatible endpoint support (OpenAI, OpenRouter, Opencode, etc.)
    # Accept both OPENAI_BASE_URL and legacy OPENAI_API_BASE env names.
    llm_base_url: str | None = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")

    # Prefer OPENAI_API_KEY but allow provider-specific alias.
    llm_api_key: str | None = os.getenv("OPENAI_API_KEY") or os.getenv("OPENCODE_API_KEY")

    # Evaluation realism control:
    # False (recommended): do NOT inject required terms into prompt input.
    # True: inject required terms verbatim into scenario (deterministic but easier to game).
    inject_required_terms_in_prompt: bool = _env_bool("POC_INJECT_REQUIRED_TERMS_IN_PROMPT", False)


def get_settings() -> Settings:
    return Settings()
