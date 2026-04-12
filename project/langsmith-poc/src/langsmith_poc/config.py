from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "poc-langsmith-dev")
    dataset_name: str = os.getenv("POC_DATASET_NAME", "ops-reflections-golden-v1")
    experiment_prefix: str = os.getenv("POC_EXPERIMENT_PREFIX", "ops-reflections")
    model_name: str = os.getenv("POC_MODEL", "gpt-4o-mini")
    use_case: str = os.getenv("POC_USE_CASE", "ops_reflection")

    # OpenAI-compatible endpoint support (OpenAI, OpenRouter, Opencode, etc.)
    # Accept both OPENAI_BASE_URL and legacy OPENAI_API_BASE env names.
    llm_base_url: str | None = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")

    # Prefer OPENAI_API_KEY but allow provider-specific alias.
    llm_api_key: str | None = os.getenv("OPENAI_API_KEY") or os.getenv("OPENCODE_API_KEY")


def get_settings() -> Settings:
    return Settings()
