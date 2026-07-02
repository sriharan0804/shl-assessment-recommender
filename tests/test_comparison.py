from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_comparison_request_returns_grounded_reply():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "What is the difference between OPQ32r and Global Skills Development Report?",
                }
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["recommendations"] == []
    assert data["end_of_conversation"] is False
    assert "comparison" in data["reply"].lower() or "difference" in data["reply"].lower()