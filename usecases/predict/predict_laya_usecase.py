from typing import Any, Dict, Optional
from usecases.predict.get_laya_router_usecase import get_laya_router


def predict_laya(
    state: Dict[str, Any],
    questions: Dict[str, Any],
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute generic prediction on the Laya router."""
    router = get_laya_router()
    return router.predict(state, questions, model=model)
