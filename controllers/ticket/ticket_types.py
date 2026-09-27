from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    ticket_id: Optional[str] = Field(default="TCK-1001", description="Unique ticket identifier")
    customer: Optional[str] = Field(default="enterprise_user", description="Customer tier or user handle")
    subject: str = Field(..., description="Subject line of the support ticket")
    body: str = Field(..., description="Full description or problem message reported by the user")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional custom key-value metadata")
    model: Optional[str] = Field(default=None, description="Optional model key override")


class TicketResponse(BaseModel):
    ticket_id: Optional[str]
    routing_decision: Optional[str]
    assigned_queue: str
    urgency_score: float
    priority_level: str
    churn_risk: str
    churn_risk_score: float
    sentiment: str
    action_recommendation: str
    raw: Optional[Dict[str, Any]] = None


class BatchTicketRequest(BaseModel):
    tickets: List[TicketRequest] = Field(..., min_length=1, description="List of tickets to process in a batch")
    model: Optional[str] = Field(default=None, description="Optional model key override")


class BatchTicketResponse(BaseModel):
    total: int
    results: List[TicketResponse]


class TicketUrgencyRequest(BaseModel):
    ticket_id: Optional[str] = Field(default=None)
    subject: str = Field(...)
    body: str = Field(...)
    model: Optional[str] = Field(default=None)


class TicketUrgencyResponse(BaseModel):
    ticket_id: Optional[str]
    urgency_score: float
    priority_level: str
    churn_risk: str
    churn_risk_score: float
    sla_risk: str
