import asyncio
from fastapi import APIRouter, HTTPException
from controllers.ticket.ticket_types import (
    TicketRequest,
    TicketResponse,
    BatchTicketRequest,
    BatchTicketResponse,
    TicketUrgencyRequest,
    TicketUrgencyResponse,
)
from services.ticket import (
    triage_ticket,
    batch_triage_tickets,
    score_ticket_urgency,
)

router = APIRouter(prefix="/ticket", tags=["Ticket Triage"])


@router.post("/triage", response_model=TicketResponse)
async def triage(ticket: TicketRequest):
    """Triage a single ticket: assigns queue, calculates urgency score, priority, churn risk, and sentiment."""
    try:
        data = ticket.model_dump()
        model = data.pop("model", None)
        return await asyncio.to_thread(triage_ticket, data, model=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-triage", response_model=BatchTicketResponse)
async def batch_triage(batch: BatchTicketRequest):
    """Triage multiple tickets in a single request for high-throughput operational intake."""
    try:
        tickets_data = [t.model_dump() for t in batch.tickets]
        return await asyncio.to_thread(batch_triage_tickets, tickets_data, model=batch.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/urgency", response_model=TicketUrgencyResponse)
async def urgency(req: TicketUrgencyRequest):
    """Sub-millisecond urgency evaluation: detects priority tiers and SLA breach probability."""
    try:
        data = req.model_dump()
        model = data.pop("model", None)
        return await asyncio.to_thread(score_ticket_urgency, data, model=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
