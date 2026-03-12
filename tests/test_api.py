from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "AI Agent Enterprise API is running!"}

def test_execute_chat():
    response = client.post("/chat", json={"user_id": "test_user", "message": "Hi"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["status"] == "success"

def test_submit_feedback():
    response = client.post("/feedback", json={"conversation_id": "test_conv", "rating": 5, "comment": "Great!"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
