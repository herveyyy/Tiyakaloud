from typing import Any, Dict, Optional
from usecases.predict.predict_laya_usecase import predict_laya

URGENCY_SCORING_QUESTIONS: Dict[str, Any] = {
    "urgency": {
        "type": "score",
        "instructions": "Evaluate how severely this issue disrupts the business operations or user workflow.",
        "criteria": [
            "minor cosmetic or question with no operational impact",
            "moderate problem with available workarounds",
            "major degradation affecting business revenue or critical features",
            "catastrophic total outage, data loss, or high-level incident",
        ],
    },
    "churn_risk": {
        "type": "noul",
        "instructions": "Is there severe danger of the customer terminating their account or requesting an immediate full refund?",
    },
}


def score_ticket_urgency(
    ticket_data: Dict[str, Any],
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Perform lightweight, rapid urgency, SLA breach risk, and churn probability evaluation."""
    result = predict_laya(state=ticket_data, questions=URGENCY_SCORING_QUESTIONS, model=model)
    answers = result.get("answers", {})

    urgency_score = float(answers.get("urgency", {}).get("score", 0.0))
    churn_noul = float(answers.get("churn_risk", {}).get("noul", 0.0))

    if urgency_score >= 0.75:
        priority = "CRITICAL"
        sla_risk = "HIGH_BREACH_RISK"
    elif urgency_score >= 0.50:
        priority = "HIGH"
        sla_risk = "MODERATE_BREACH_RISK"
    elif urgency_score >= 0.25:
        priority = "MEDIUM"
        sla_risk = "NORMAL"
    else:
        priority = "LOW"
        sla_risk = "MINIMAL"

    return {
        "ticket_id": ticket_data.get("ticket_id"),
        "urgency_score": round(urgency_score, 4),
        "priority_level": priority,
        "churn_risk": f"{churn_noul:.1%}",
        "churn_risk_score": round(churn_noul, 4),
        "sla_risk": sla_risk,
    }
