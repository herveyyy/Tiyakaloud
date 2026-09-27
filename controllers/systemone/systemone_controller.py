import asyncio
from fastapi import APIRouter, HTTPException
from controllers.systemone.systemone_types import SystemOneRequest
from services.systemone.systemone_service import run_systemone

router = APIRouter(prefix="/v1", tags=["System 1 Protocol"])


@router.post("/systemone")
async def systemone(payload: SystemOneRequest):
    """Standard Laya /v1/systemone compatible endpoint."""
    try:
        result = await asyncio.to_thread(
            run_systemone,
            payload.state,
            payload.questions,
            payload.model,
        )
        print("Prediction Result:", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
