from typing import Any, Dict
from usecases.predict.predict_laya_usecase import predict_laya

DEFAULT_TICKET_QUESTIONS: Dict[str, Any] = {
    "queue": {
        "type": "choice",
        "instructions": "Which engineering queue owns this ticket?",
        "criteria": {
            "infrastructure": "server outages, network downtime, database failures",
            "billing": "refunds, SLA credits, invoice disputes",
            "security": "breaches, vulnerability reports",
            "support": "general customer inquiries",
        },
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this ticket?",
        "criteria": ["low priority", "medium", "high priority", "critical blocker"],
    },
    "churn_risk": {
        "type": "noul",
        "instructions": "Does the customer threaten to cancel or express severe churn intent?",
    },
}


def triage_ticket(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
    """Triage, route, and score a customer support ticket."""
    result = predict_laya(state=ticket_data, questions=DEFAULT_TICKET_QUESTIONS)
    answers = result.get("answers", {})
    routing = result.get("routing", {})

    return {
        "ticket_id": ticket_data.get("ticket_id"),
        "routing_decision": routing.get("model"),
        "assigned_queue": answers.get("queue", {}).get("choice"),
        "urgency_score": answers.get("urgency", {}).get("score"),
        "churn_risk": f"{answers.get('churn_risk', {}).get('noul', 0.0):.1%}",
        "raw": result,
    }
