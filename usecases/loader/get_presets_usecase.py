from typing import Any, Dict
import laya.presets as lp
from usecases.loader.load_custom_preset_usecase import get_custom_presets_registry


def get_presets() -> Dict[str, Any]:
    """List built-in standard question presets and dynamically registered custom presets."""
    built_in = {
        "triage": list(lp.triage_questions().keys()) if hasattr(lp, "triage_questions") else [],
        "email": list(lp.email_questions().keys()) if hasattr(lp, "email_questions") else [],
        "guard": list(lp.guard_questions().keys()) if hasattr(lp, "guard_questions") else [],
        "moderation": list(lp.moderation_questions().keys()) if hasattr(lp, "moderation_questions") else [],
        "router": list(lp.router_questions().keys()) if hasattr(lp, "router_questions") else [],
    }

    custom = {
        name: list(questions.keys())
        for name, questions in get_custom_presets_registry().items()
    }

    return {
        "built_in_presets": built_in,
        "custom_presets": custom,
        "total_custom_presets": len(custom),
    }
