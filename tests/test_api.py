
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


def test_environment_plan_endpoint():
    response = client.post(
        "/environments/plan",
        json={"environment": "dev"},
    )

    assert response.status_code == 200
    assert response.json()["project"] == "CloudForge"
    assert response.json()["environment"] == "dev"
    assert response.json()["application_name"] == "sample-app"
    assert response.json()["aws_region"] == "us-east-1"
    assert response.json()["provisioning"] is False


def test_environment_plan_accepts_staging_and_prod():
    for environment in ["staging", "prod"]:
        response = client.post(
            "/environments/plan",
            json={"environment": environment},
        )

        assert response.status_code == 200
        assert response.json()["environment"] == environment


def test_environment_plan_rejects_invalid_environment():
    response = client.post(
        "/environments/plan",
        json={"environment": "test"},
    )

    assert response.status_code == 422


def test_environment_plan_rejects_invalid_application_name():
    response = client.post(
        "/environments/plan",
        json={
            "environment": "dev",
            "application_name": "My App!",
        },
    )

    assert response.status_code == 422

def test_environment_plan_rejects_invalid_region():
    response = client.post(
        "/environments/plan",
        json={
            "environment": "dev",
            "aws_region": "invalid-region",
        },
    )

    assert response.status_code == 422