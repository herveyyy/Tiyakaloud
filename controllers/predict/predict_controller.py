import asyncio
from fastapi import APIRouter, HTTPException
from controllers.predict.predict_types import (
    PredictRequest,
    TicketRequest,
    TicketResponse,
)
from services.predict.predict_service import (
    predict_laya,
    triage_ticket,
    DEFAULT_TICKET_QUESTIONS,
)

router = APIRouter(tags=["Prediction"])


@router.post("/predict")
async def predict(payload: PredictRequest):
    """General-purpose inference endpoint: accepts any state and questions."""
    questions = payload.questions or DEFAULT_TICKET_QUESTIONS
    try:
        payload = await asyncio.to_thread(
            predict_laya,
            payload.state,
            questions,
            payload.model,
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/ticket", response_model=TicketResponse)
async def predict_ticket(ticket: TicketRequest):
    """Convenience endpoint: classifies and scores a support ticket with the default criteria."""
    try:
        ticket_data = ticket.model_dump()
        return await asyncio.to_thread(triage_ticket, ticket_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
