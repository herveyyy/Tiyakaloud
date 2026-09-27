from fastapi import APIRouter
from controllers.health.health_types import HealthResponse
from services.health.health_service import get_health_status

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health():
    """Returns the operational status, loaded models, and device of the Laya router."""
    return get_health_status()
