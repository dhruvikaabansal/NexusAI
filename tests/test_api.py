from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to HRCentral API"}

def test_login_demo():
    response = client.post("/auth/login", json={"email": "alice@acme.com", "password": "demo"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@acme.com"
    assert data["role"] == "CEO"

def test_dashboard_ceo():
    response = client.get("/dashboards/CEO")
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "CEO"
    assert len(data["kpis"]) > 0
    assert len(data["charts"]) > 0

def test_dashboard_coo():
    response = client.get("/dashboards/COO")
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "COO"
    # Check for specific COO KPI labels
    labels = [k["label"] for k in data["kpis"]]
    assert "Avg Throughput" in labels

def test_chatbot_response():
    response = client.post("/chat/", json={
        "user_id": "test_user",
        "role": "CEO",
        "query": "What is the revenue?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "revenue" in data["answer"].lower() or "sales" in data["answer"].lower()
    assert len(data["suggested_followups"]) > 0
