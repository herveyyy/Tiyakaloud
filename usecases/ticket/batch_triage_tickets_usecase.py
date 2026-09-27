from typing import Any, Dict, List, Optional
from usecases.ticket.triage_ticket_usecase import triage_ticket


def batch_triage_tickets(
    tickets: List[Dict[str, Any]],
    custom_questions: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Triage multiple customer support tickets in a single request batch."""
    if not tickets:
        return {"total": 0, "results": []}

    results: List[Dict[str, Any]] = []
    for item in tickets:
        triage_result = triage_ticket(item, custom_questions=custom_questions, model=model)
        results.append(triage_result)

    return {
        "total": len(results),
        "results": results,
    }
