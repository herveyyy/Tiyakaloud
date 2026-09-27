from typing import Any, Dict
from usecases.predict.get_laya_router_usecase import get_laya_router


def get_health_status() -> Dict[str, Any]:
    """Retrieve health and loaded model status for the Laya engine."""
    router = get_laya_router()
    return {
        "status": "ok",
        "loaded_models": getattr(router, "loaded", []),
        "device": str(getattr(router, "device", "cpu")),
    }
