from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_java_developer_recommendations():
    response = client.post(
        "/chat",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "I am hiring a mid-level Java developer with backend and SQL skills",
                }
            ]
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["recommendations"]) > 0
    assert len(data["recommendations"]) <= 10
    assert data["end_of_conversation"] is True
    

    for item in data["recommendations"]:
        assert item["name"]
        assert item["url"].startswith("https://www.shl.com/")
        assert item["test_type"]