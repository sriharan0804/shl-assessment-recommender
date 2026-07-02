from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_off_topic_refusal():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {"role": "user", "content": "Give me interview questions for Java developer"}
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["recommendations"] == []
    assert "SHL assessment" in data["reply"]
    assert data["end_of_conversation"] is False