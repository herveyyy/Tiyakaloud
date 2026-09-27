import os
from typing import Optional
from laya import Router

_router_instance: Optional[Router] = None


def get_laya_router() -> Router:
    """Singleton getter for the Laya Router instance."""
    global _router_instance
    if _router_instance is None:
        preload = os.environ.get("LAYA_PRELOAD", "0").lower() in ("true", "1", "yes")
        _router_instance = Router(preload=preload)
    return _router_instance
