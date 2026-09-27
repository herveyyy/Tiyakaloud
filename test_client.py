"""Test script for Laya Server.

Supports:
1. Live testing against `laya-serve` or `main.py` at http://localhost:8000
2. In-memory testing if no server is running
3. Automatic testing of standard `/v1/systemone` endpoint as well as `/predict/ticket`
"""

import sys
import json
import urllib.request
import urllib.error

SERVER_URL = "http://localhost:8000"

TICKET_PAYLOAD = {
    "state": {
        "ticket_id": "TCK-8821",
        "customer": "enterprise_user",
        "subject": "System downtime and billing dispute",
        "body": "Our production API has been failing since 6 AM. We lost critical transactions. We demand an immediate SLA refund."
    },
    "questions": {
        "queue": {
            "type": "choice",
            "instructions": "Which engineering queue owns this ticket?",
            "criteria": {
                "infrastructure": "server outages, network downtime, database failures",
                "billing": "refunds, SLA credits, invoice disputes",
                "security": "breaches, vulnerability reports",
                "support": "general customer inquiries"
            }
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent is this ticket?",
            "criteria": ["low priority", "medium", "high priority", "critical blocker"]
        },
        "churn_risk": {
            "type": "noul",
            "instructions": "Does the customer threaten to cancel or express severe churn intent?"
        }
    }
}


def is_live_server_running(url: str) -> bool:
    try:
        req = urllib.request.Request(f"{url}/health")
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def test_live_server(base_url: str):
    print(f"--> Connected to live server at: {base_url}\n")
    
    # 1. Health check
    print("[1] Testing GET /health ...")
    req = urllib.request.Request(f"{base_url}/health")
    with urllib.request.urlopen(req) as resp:
        health_data = json.loads(resp.read().decode())
        print(f"    Status: {resp.status}")
        print(f"    Loaded Models: {health_data.get('loaded', health_data.get('loaded_models'))}")
        print(f"    Device       : {health_data.get('device')}")

    # 2. Standard Laya Protocol (/v1/systemone)
    print("\n[2] Testing POST /v1/systemone (Standard Laya Protocol) ...")
    payload_bytes = json.dumps(TICKET_PAYLOAD).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/v1/systemone",
        data=payload_bytes,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        answers = res.get("answers", {})
        routing = res.get("routing", {})
        print(f"    Status: {resp.status}")
        print(f"    Routing Decision : {routing.get('model')}")
        print(f"    Assigned Queue   : {answers.get('queue', {}).get('choice')}")
        print(f"    Urgency Score    : {answers.get('urgency', {}).get('score')}")
        print(f"    Churn Risk       : {answers.get('churn_risk', {}).get('noul', 0.0):.1%}")

    # 3. Check if extended endpoints (/predict/ticket) from main.py exist
    print("\n[3] Testing POST /predict/ticket (Convenience endpoint in main.py) ...")
    ticket_simple = TICKET_PAYLOAD["state"]
    req = urllib.request.Request(
        f"{base_url}/predict/ticket",
        data=json.dumps(ticket_simple).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"    Status: {resp.status}")
            print(f"    Assigned Queue   : {data.get('assigned_queue')}")
            print(f"    Urgency Score    : {data.get('urgency_score')}")
            print(f"    Churn Risk       : {data.get('churn_risk')}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"    Note: /predict/ticket returned 404 (You are currently running 'laya-serve').")
            print(f"    To enable this endpoint, run: python laya/main.py")
        else:
            raise


def test_in_memory():
    print("--> No live server running. Testing in-memory via FastAPI TestClient ...\n")
    from fastapi.testclient import TestClient
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    import main

    client = TestClient(main.app)

    print("[1] Testing GET /health ...")
    resp = client.get("/health")
    print(f"    Status: {resp.status_code}")
    print(f"    Data  : {resp.json()}")

    print("\n[2] Testing POST /v1/systemone ...")
    resp = client.post("/v1/systemone", json=TICKET_PAYLOAD)
    res = resp.json()
    answers = res.get("answers", {})
    routing = res.get("routing", {})
    print(f"    Status: {resp.status_code}")
    print(f"    Routing Decision : {routing.get('model')}")
    print(f"    Assigned Queue   : {answers.get('queue', {}).get('choice')}")
    print(f"    Urgency Score    : {answers.get('urgency', {}).get('score')}")
    print(f"    Churn Risk       : {answers.get('churn_risk', {}).get('noul', 0.0):.1%}")

    print("\n[3] Testing POST /predict/ticket ...")
    resp = client.post("/predict/ticket", json=TICKET_PAYLOAD["state"])
    data = resp.json()
    print(f"    Status: {resp.status_code}")
    print(f"    Assigned Queue   : {data.get('assigned_queue')}")
    print(f"    Urgency Score    : {data.get('urgency_score')}")
    print(f"    Churn Risk       : {data.get('churn_risk')}")


def main():
    if is_live_server_running(SERVER_URL):
        test_live_server(SERVER_URL)
    else:
        test_in_memory()
    print("\n==========================================")
    print("  All tests completed successfully!")
    print("==========================================")


if __name__ == "__main__":
    main()
