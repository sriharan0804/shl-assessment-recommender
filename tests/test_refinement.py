from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_refinement_keeps_context_and_returns_recommendations():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "I am hiring a mid-level Java developer with backend skills",
                },
                {
                    "role": "assistant",
                    "content": "Based on the role details, here are some SHL assessments.",
                },
                {
                    "role": "user",
                    "content": "Actually add personality tests also",
                },
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0
    assert "updated" in data["reply"].lower() or "added constraint" in data["reply"].lower()