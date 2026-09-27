import time
from typing import Any, Dict, Optional
from usecases.predict.get_laya_router_usecase import get_laya_router


def load_model(
    model_name: str,
    custom_repo: Optional[str] = None,
    subfolder: Optional[str] = None,
) -> Dict[str, Any]:
    """Dynamically load, register, or warm up a standard or custom Laya ModernBERT model."""
    if not model_name or not model_name.strip():
        raise ValueError("model_name cannot be empty")

    name = model_name.strip()
    router = get_laya_router()

    # If custom repo is supplied, register it in the router's model registry
    if custom_repo is not None:
        router.models[name] = (custom_repo.strip(), subfolder.strip() if subfolder else None)

    start_time = time.perf_counter()
    agent = router.load(name)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "success": True,
        "model_name": name,
        "loaded_models": list(router.loaded),
        "device": str(router.device),
        "load_time_ms": round(elapsed_ms, 2),
        "message": f"Model '{name}' loaded into memory successfully.",
    }
