import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.main import app  # noqa: E402


client = TestClient(app)


def check_trace(trace: dict) -> bool:
    response = client.post("/chat", json={"messages": trace["messages"]})

    if response.status_code != 200:
        print(f"❌ {trace['name']}: status {response.status_code}")
        return False

    data = response.json()
    expected = trace["expected"]

    if "reply" not in data or "recommendations" not in data or "end_of_conversation" not in data:
        print(f"❌ {trace['name']}: invalid schema")
        return False

    if expected.get("recommendations_empty") is True and data["recommendations"]:
        print(f"❌ {trace['name']}: expected empty recommendations")
        return False

    if expected.get("recommendations_empty") is False and not data["recommendations"]:
        print(f"❌ {trace['name']}: expected recommendations")
        return False

    max_recs = expected.get("max_recommendations")
    if max_recs and len(data["recommendations"]) > max_recs:
        print(f"❌ {trace['name']}: too many recommendations")
        return False

    contains = expected.get("reply_contains_any", [])
    if contains and not any(word.lower() in data["reply"].lower() for word in contains):
        print(f"❌ {trace['name']}: reply did not contain expected words")
        return False

    print(f"✅ {trace['name']}")
    return True


def main():
    trace_path = Path("evals/sample_traces.json")

    with trace_path.open("r", encoding="utf-8") as file:
        traces = json.load(file)

    passed = sum(check_trace(trace) for trace in traces)

    print(f"\nPassed {passed}/{len(traces)} traces")

    if passed != len(traces):
        raise SystemExit(1)


if __name__ == "__main__":
    main()