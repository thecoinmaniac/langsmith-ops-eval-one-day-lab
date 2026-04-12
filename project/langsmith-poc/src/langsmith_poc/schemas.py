from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class DraftInput(BaseModel):
    id: str
    input: str
    expected_style: str = "operator-first"
    must_include: List[str] = Field(default_factory=list)


class DraftOutput(BaseModel):
    text: str
