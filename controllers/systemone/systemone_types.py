from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class SystemOneRequest(BaseModel):
    state: Dict[str, Any] = Field(
        default_factory=dict,
        description="The contextual state or entity payload",
    )
    questions: Dict[str, Any] = Field(
        ...,
        description="Questions map adhering to Laya System 1 primitives (choice, score, noul)",
    )
    model: Optional[str] = Field(
        default=None,
        description="Optional model identifier ('english', 'multilingual', 'typed-decisions')",
    )
