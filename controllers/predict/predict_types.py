from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    state: Dict[str, Any] = Field(
        ...,
        description="Arbitrary input state (e.g., ticket data, user query, message, or document)",
        json_schema_extra={
            "example": {
                "ticket_id": "TCK-8821",
                "customer": "enterprise_user",
                "subject": "System downtime and billing dispute",
                "body": "Our production API has been failing since 6 AM. We lost critical transactions. We demand an immediate SLA refund.",
            }
        },
    )
    questions: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional custom questions dictionary. If omitted, uses default ticket triage questions.",
    )
    model: Optional[str] = Field(
        default=None,
        description="Optional model identifier ('english', 'multilingual', 'typed-decisions').",
    )


class TicketRequest(BaseModel):
    ticket_id: Optional[str] = Field(default="TCK-8821", example="TCK-8821")
    customer: Optional[str] = Field(default="enterprise_user", example="enterprise_user")
    subject: str = Field(
        default="System downtime and billing dispute",
        example="System downtime and billing dispute",
    )
    body: str = Field(
        default="Our production API has been failing since 6 AM. We lost critical transactions. We demand an immediate SLA refund.",
        example="Our production API has been failing since 6 AM. We lost critical transactions. We demand an immediate SLA refund.",
    )


class TicketResponse(BaseModel):
    ticket_id: Optional[str]
    routing_decision: Optional[str]
    assigned_queue: Optional[str]
    urgency_score: Optional[float]
    churn_risk: Optional[str]
    raw: Dict[str, Any]
