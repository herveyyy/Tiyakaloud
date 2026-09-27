from typing import Any, Dict, Optional
from usecases.loader import (
    load_model as _load_model,
    unload_model as _unload_model,
    get_model_status as _get_model_status,
    load_custom_preset as _load_custom_preset,
    get_presets as _get_presets,
)


def load_model(
    model_name: str,
    custom_repo: Optional[str] = None,
    subfolder: Optional[str] = None,
) -> Dict[str, Any]:
    """Service entrypoint for dynamic model loading / registration."""
    return _load_model(model_name, custom_repo=custom_repo, subfolder=subfolder)


def unload_model(model_name: Optional[str] = None) -> Dict[str, Any]:
    """Service entrypoint for evicting model weights from memory."""
    return _unload_model(model_name=model_name)


def get_model_status() -> Dict[str, Any]:
    """Service entrypoint for checking available and active in-memory models."""
    return _get_model_status()


def load_custom_preset(preset_name: str, questions: Dict[str, Any]) -> Dict[str, Any]:
    """Service entrypoint for dynamically registering question presets."""
    return _load_custom_preset(preset_name, questions)


def get_presets() -> Dict[str, Any]:
    """Service entrypoint for listing built-in and custom question presets."""
    return _get_presets()


__all__ = [
    "load_model",
    "unload_model",
    "get_model_status",
    "load_custom_preset",
    "get_presets",
]
