from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_vague_query_asks_clarification():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {"role": "user", "content": "I need an assessment"}
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["recommendations"] == []
    assert "role" in data["reply"].lower() or "skills" in data["reply"].lower()
    assert data["end_of_conversation"] is False


def test_partial_context_asks_followup():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {"role": "user", "content": "Hiring a developer"}
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["recommendations"] == []
    assert "seniority" in data["reply"].lower() or "skills" in data["reply"].lower()
    assert data["end_of_conversation"] is False