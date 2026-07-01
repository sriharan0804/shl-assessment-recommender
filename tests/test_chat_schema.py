from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_schema():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {"role": "user", "content": "I need an assessment"}
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "reply" in data
    assert "recommendations" in data
    assert "end_of_conversation" in data
    assert isinstance(data["reply"], str)
    assert isinstance(data["recommendations"], list)
    assert isinstance(data["end_of_conversation"], bool)