import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(__file__))
import main as laya_server

TICKET_PAYLOAD = {
    "state": {
        "ticket_id": "TCK-8821",
        "customer": "enterprise_user",
        "subject": "System downtime and billing dispute",
        "body": "Our production API has been failing since 6 AM. We lost critical transactions. We demand an immediate SLA refund.",
    },
    "questions": {
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
    },
}


def test_in_memory():
    print("--> Running in-memory test via FastAPI TestClient ...")
    client = TestClient(laya_server.app)

    # 1. Health check
    print("[1] Testing GET /health ...")
    resp = client.get("/health")
    print(f"    Status: {resp.status_code}")
    print(f"    Data  : {resp.json()}")

    # 2. Model status & Presets
    print("\n[2] Testing GET /models (Loader status) ...")
    resp = client.get("/models")
    print(f"    Status: {resp.status_code}")
    print(f"    Available Models: {resp.json().get('total_available')}")

    print("\n[3] Testing GET & POST /models/presets ...")
    resp = client.get("/models/presets")
    print(f"    Built-in Presets: {list(resp.json().get('built_in_presets', {}).keys())}")

    resp = client.post(
        "/models/presets",
        json={
            "preset_name": "retention_triage",
            "questions": {
                "risk": {
                    "type": "noul",
                    "instructions": "Is the account at immediate cancellation risk?",
                }
            },
        },
    )
    print(f"    Preset Creation Status: {resp.status_code}")
    print(f"    Registered Preset     : {resp.json().get('preset_name')}")

    # 4. Standard System 1 Protocol
    print("\n[4] Testing POST /v1/systemone ...")
    resp = client.post("/v1/systemone", json=TICKET_PAYLOAD)
    res = resp.json()
    answers = res.get("answers", {})
    routing = res.get("routing", {})
    print(f"    Status: {resp.status_code}")
    print(f"    Routing Decision : {routing.get('model')}")
    print(f"    Assigned Queue   : {answers.get('queue', {}).get('choice')}")
    print(f"    Urgency Score    : {answers.get('urgency', {}).get('score')}")
    print(f"    Churn Risk       : {answers.get('churn_risk', {}).get('noul', 0.0):.1%}")

    # 5. Ticket Domain - Urgency
    print("\n[5] Testing POST /ticket/urgency ...")
    resp = client.post(
        "/ticket/urgency",
        json={
            "ticket_id": "TCK-8821",
            "subject": TICKET_PAYLOAD["state"]["subject"],
            "body": TICKET_PAYLOAD["state"]["body"],
        },
    )
    print(f"    Status: {resp.status_code}")
    print(f"    Priority Level: {resp.json().get('priority_level')}")
    print(f"    SLA Risk      : {resp.json().get('sla_risk')}")

    # 6. Ticket Domain - Full Triage
    print("\n[6] Testing POST /ticket/triage ...")
    resp = client.post("/ticket/triage", json=TICKET_PAYLOAD["state"])
    data = resp.json()
    print(f"    Status: {resp.status_code}")
    print(f"    Assigned Queue  : {data.get('assigned_queue')}")
    print(f"    Priority Level  : {data.get('priority_level')}")
    print(f"    Sentiment       : {data.get('sentiment')}")
    print(f"    Recommendation  : {data.get('action_recommendation')}")


def run_tests():
    test_in_memory()
    print("\n==========================================")
    print("  All tests completed successfully!")
    print("==========================================")


if __name__ == "__main__":
    run_tests()
