from typing import List
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    loaded_models: List[str] = Field(..., example=["english", "multilingual", "typed-decisions"])
    device: str = Field(..., example="cpu")
