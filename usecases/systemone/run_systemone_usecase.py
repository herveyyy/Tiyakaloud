from typing import Any, Dict, Optional
from usecases.predict.predict_laya_usecase import predict_laya


def run_systemone(
    state: Dict[str, Any],
    questions: Dict[str, Any],
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute prediction, print individual values, and return direct predictions."""
    result = predict_laya(state=state, questions=questions, model=model)
    answers = result.get("answers", {})
    routing = result.get("routing", {})

    extracted = {}
    for key, item in answers.items():
        if isinstance(item, dict):
            if "choice" in item:
                extracted[key] = item["choice"]
            elif "noul" in item:
                extracted[key] = item["noul"]
            elif "score" in item:
                extracted[key] = item["score"]
            else:
                extracted[key] = item
        else:
            extracted[key] = item

    routing_model = routing.get("model")
    if routing_model:
        extracted["routing_model"] = routing_model

    # Explicit individual prints
    print("\n--- Extracted Predictions ---")
    for key, val in extracted.items():
        print(f"{key}: {val}")
    print("-----------------------------\n")

    return extracted
