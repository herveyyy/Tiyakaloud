from typing import Any, Dict, List, Optional
from usecases.ticket import (
    triage_ticket as _triage_ticket,
    batch_triage_tickets as _batch_triage_tickets,
    score_ticket_urgency as _score_ticket_urgency,
    DEFAULT_TICKET_TRIAGE_QUESTIONS,
    URGENCY_SCORING_QUESTIONS,
)


def triage_ticket(
    ticket_data: Dict[str, Any],
    custom_questions: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Service entrypoint for triaging, routing, and scoring a support ticket."""
    return _triage_ticket(ticket_data, custom_questions=custom_questions, model=model)


def batch_triage_tickets(
    tickets: List[Dict[str, Any]],
    custom_questions: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Service entrypoint for batch triage across multiple tickets."""
    return _batch_triage_tickets(tickets, custom_questions=custom_questions, model=model)


def score_ticket_urgency(
    ticket_data: Dict[str, Any],
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Service entrypoint for urgency scoring and SLA breach risk."""
    return _score_ticket_urgency(ticket_data, model=model)


__all__ = [
    "triage_ticket",
    "batch_triage_tickets",
    "score_ticket_urgency",
    "DEFAULT_TICKET_TRIAGE_QUESTIONS",
    "URGENCY_SCORING_QUESTIONS",
]
