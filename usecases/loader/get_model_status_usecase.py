from typing import Any, Dict
from usecases.predict.get_laya_router_usecase import get_laya_router


def get_model_status() -> Dict[str, Any]:
    """Return comprehensive lifecycle status of models registered and currently active in memory."""
    router = get_laya_router()
    available = {}
    for name, spec in router.models.items():
        repo, sub = spec
        available[name] = {
            "repository": repo,
            "subfolder": sub,
            "is_loaded": name in router.loaded,
        }

    return {
        "device": str(router.device),
        "total_available": len(available),
        "total_loaded": len(router.loaded),
        "loaded_models": list(router.loaded),
        "models": available,
    }
