from typing import Any, Dict, Optional
from usecases.predict.get_laya_router_usecase import get_laya_router


def unload_model(model_name: Optional[str] = None) -> Dict[str, Any]:
    """Evict one or all loaded ModernBERT models from RAM/VRAM to free memory resources."""
    router = get_laya_router()
    target = model_name.strip() if model_name else None

    router.unload(target)

    return {
        "success": True,
        "unloaded": target or "ALL",
        "remaining_models": list(router.loaded),
        "message": f"Successfully unloaded '{target or 'all models'}' from memory.",
    }
