from typing import Any, Dict, Optional
from usecases.predict.predict_laya_usecase import predict_laya

DEFAULT_TICKET_TRIAGE_QUESTIONS: Dict[str, Any] = {
    "queue": {
        "type": "choice",
        "instructions": "Which engineering or support department should handle this ticket?",
        "criteria": {
            "infrastructure": "server outages, network downtime, database failures, latency spikes",
            "billing": "refunds, SLA credits, invoice disputes, payment processing errors",
            "security": "unauthorized access, vulnerabilities, credential leaks, data breaches",
            "support": "general questions, documentation requests, feature guidance, login issues",
        },
    },
    "urgency": {
        "type": "score",
        "instructions": "Rate how urgent this ticket is based on business disruption and user impact.",
        "criteria": ["low priority", "medium priority", "high priority", "critical blocker"],
    },
    "churn_risk": {
        "type": "noul",
        "instructions": "Does the customer express intent to cancel, request a refund, or threaten to switch providers?",
    },
    "sentiment": {
        "type": "choice",
        "instructions": "What is the emotional tone and frustration level of the customer?",
        "criteria": {
            "positive": "satisfied, grateful, appreciative tone",
            "neutral": "factual, objective, transactional inquiry",
            "frustrated": "annoyed, experiencing recurring issues, expressing dissatisfaction",
            "angry": "hostile, demanding escalation, aggressive demands",
        },
    },
}


def _calculate_priority_level(urgency_score: float, churn_noul: float) -> str:
    if urgency_score >= 0.75 or (urgency_score >= 0.5 and churn_noul >= 0.6):
        return "CRITICAL"
    elif urgency_score >= 0.50 or churn_noul >= 0.5:
        return "HIGH"
    elif urgency_score >= 0.25:
        return "MEDIUM"
    return "LOW"


def _generate_recommendation(queue: str, priority: str, churn_noul: float) -> str:
    if priority == "CRITICAL":
        return f"Immediate on-call page to {queue.upper()} lead; notify Customer Success."
    elif churn_noul >= 0.5:
        return f"Route to {queue} with senior support representative; trigger retention outreach."
    elif priority == "HIGH":
        return f"Assign to {queue} queue with 2-hour SLA response target."
    return f"Standard routing to {queue} queue."


def triage_ticket(
    ticket_data: Dict[str, Any],
    custom_questions: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Triage, classify, and score a customer support ticket using Laya."""
    questions = custom_questions or DEFAULT_TICKET_TRIAGE_QUESTIONS
    result = predict_laya(state=ticket_data, questions=questions, model=model)
    answers = result.get("answers", {})
    routing = result.get("routing", {})

    urgency_data = answers.get("urgency", {})
    urgency_score = float(urgency_data.get("score", 0.0))

    churn_data = answers.get("churn_risk", {})
    churn_noul = float(churn_data.get("noul", 0.0))

    queue_data = answers.get("queue", {})
    assigned_queue = str(queue_data.get("choice", "support"))

    sentiment_data = answers.get("sentiment", {})
    detected_sentiment = str(sentiment_data.get("choice", "neutral"))

    priority_level = _calculate_priority_level(urgency_score, churn_noul)
    recommendation = _generate_recommendation(assigned_queue, priority_level, churn_noul)

    return {
        "ticket_id": ticket_data.get("ticket_id"),
        "routing_decision": routing.get("model", "default"),
        "assigned_queue": assigned_queue,
        "urgency_score": round(urgency_score, 4),
        "priority_level": priority_level,
        "churn_risk": f"{churn_noul:.1%}",
        "churn_risk_score": round(churn_noul, 4),
        "sentiment": detected_sentiment,
        "action_recommendation": recommendation,
        "raw": result,
    }
