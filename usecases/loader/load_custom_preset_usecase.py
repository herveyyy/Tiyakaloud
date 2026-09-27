from typing import Any, Dict

# In-memory registry for dynamic custom question presets
_CUSTOM_PRESETS: Dict[str, Dict[str, Any]] = {}


def get_custom_presets_registry() -> Dict[str, Dict[str, Any]]:
    return _CUSTOM_PRESETS


def load_custom_preset(preset_name: str, questions: Dict[str, Any]) -> Dict[str, Any]:
    """Register or update a custom questions preset for dynamic reuse in System 1 inferences."""
    if not preset_name or not preset_name.strip():
        raise ValueError("preset_name cannot be empty")
    if not questions or not isinstance(questions, dict):
        raise ValueError("questions must be a non-empty dictionary")

    # Validate structure of each question
    valid_types = {"choice", "score", "noul"}
    for q_key, q_val in questions.items():
        if not isinstance(q_val, dict):
            raise ValueError(f"Question '{q_key}' definition must be a dictionary")
        q_type = q_val.get("type")
        if q_type not in valid_types:
            raise ValueError(f"Question '{q_key}' has invalid type '{q_type}'. Must be one of {valid_types}")
        if "instructions" not in q_val:
            raise ValueError(f"Question '{q_key}' is missing required 'instructions' string")

    name = preset_name.strip().lower()
    _CUSTOM_PRESETS[name] = questions

    return {
        "success": True,
        "preset_name": name,
        "question_keys": list(questions.keys()),
        "total_questions": len(questions),
        "message": f"Custom preset '{name}' registered successfully.",
    }
