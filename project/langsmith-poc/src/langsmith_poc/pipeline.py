from __future__ import annotations

from pathlib import Path
from langsmith import traceable
from langchain_openai import ChatOpenAI

from .config import get_settings


PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(version: str = "v1") -> str:
    filename = "ops_brief_v1.txt" if version == "v1" else "ops_brief_v2.txt"
    return (PROMPT_DIR / filename).read_text(encoding="utf-8")


@traceable(name="generate_ops_reflection_brief")
def generate_ops_reflection_brief(user_input: str, prompt_version: str = "v1") -> str:
    settings = get_settings()
    prompt = load_prompt(prompt_version).format(user_input=user_input)

    llm_kwargs = {
        "model": settings.model_name,
        "temperature": 0.3,
    }
    if settings.llm_base_url:
        llm_kwargs["base_url"] = settings.llm_base_url
    if settings.llm_api_key:
        llm_kwargs["api_key"] = settings.llm_api_key

    llm = ChatOpenAI(**llm_kwargs)
    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))
