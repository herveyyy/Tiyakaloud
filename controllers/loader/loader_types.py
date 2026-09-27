from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LoadModelRequest(BaseModel):
    model_name: str = Field(..., description="Target model name identifier (e.g. 'english', 'multilingual', 'typed-decisions', or custom name)")
    custom_repo: Optional[str] = Field(default=None, description="Optional custom Hugging Face repository identifier (e.g. 'org/custom-model')")
    subfolder: Optional[str] = Field(default=None, description="Optional subfolder inside the repository")


class LoadModelResponse(BaseModel):
    success: bool
    model_name: str
    loaded_models: List[str]
    device: str
    load_time_ms: float
    message: str


class UnloadModelRequest(BaseModel):
    model_name: Optional[str] = Field(default=None, description="Model to unload, or null to evict all loaded models")


class UnloadModelResponse(BaseModel):
    success: bool
    unloaded: str
    remaining_models: List[str]
    message: str


class ModelStatusResponse(BaseModel):
    device: str
    total_available: int
    total_loaded: int
    loaded_models: List[str]
    models: Dict[str, Any]


class CustomPresetRequest(BaseModel):
    preset_name: str = Field(..., description="Unique alphanumeric identifier for this preset")
    questions: Dict[str, Any] = Field(..., description="Questions schema mapping question key to type, instructions, criteria")


class CustomPresetResponse(BaseModel):
    success: bool
    preset_name: str
    question_keys: List[str]
    total_questions: int
    message: str


class PresetsListResponse(BaseModel):
    built_in_presets: Dict[str, List[str]]
    custom_presets: Dict[str, List[str]]
    total_custom_presets: int
