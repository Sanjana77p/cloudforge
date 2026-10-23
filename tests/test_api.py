
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


def test_environment_plan_returns_instance_size_and_budget():
    response = client.post(
        "/environments/plan",
        json={
            "environment": "dev",
            "instance_size": "medium",
            "monthly_budget_usd": 4.5,
        },
    )

    assert response.status_code == 200
    assert response.json()["instance_size"] == "medium"
    assert response.json()["monthly_budget_usd"] == 4.5


def test_environment_plan_rejects_budget_above_limit():
    response = client.post(
        "/environments/plan",
        json={
            "environment": "dev",
            "monthly_budget_usd": 6.0,
        },
    )

    assert response.status_code == 422


def test_environment_plan_rejects_invalid_instance_size():
    response = client.post(
        "/environments/plan",
        json={
            "environment": "dev",
            "instance_size": "large",
        },
    )

    assert response.status_code == 422


def test_cost_estimate_within_budget():
    response = client.post(
        "/cost/estimate",
        json={
            "environment": "dev",
            "aws_region": "us-east-1",
            "application_name": "sample-app",
            "instance_size": "small",
            "monthly_budget_usd": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["estimated_monthly_cost_usd"] == 3.0
    assert data["budget_status"] == "within_budget"
    assert data["budget_exceeded"] is False
    assert data["remaining_budget_usd"] == 2.0
    assert data["estimate_type"] == "illustrative_demo_estimate"


def test_cost_estimate_over_budget():
    response = client.post(
        "/cost/estimate",
        json={
            "environment": "prod",
            "aws_region": "us-east-1",
            "application_name": "sample-app",
            "instance_size": "medium",
            "monthly_budget_usd": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["estimated_monthly_cost_usd"] == 20.0
    assert data["budget_status"] == "over_budget"
    assert data["budget_exceeded"] is True
    assert data["remaining_budget_usd"] == -15.0
    assert data["estimate_type"] == "illustrative_demo_estimate"


def test_cost_estimate_rejects_budget_above_limit():
    response = client.post(
        "/cost/estimate",
        json={
            "environment": "dev",
            "aws_region": "us-east-1",
            "application_name": "sample-app",
            "instance_size": "small",
            "monthly_budget_usd": 10,
        },
    )

    assert response.status_code == 422
