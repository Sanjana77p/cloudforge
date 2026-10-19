
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["project"] == "CloudForge"
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_platform_endpoint():
    response = client.get("/platform")

    assert response.status_code == 200
    assert response.json()["name"] == "CloudForge"
    assert "Security guardrails" in response.json()["features"]
