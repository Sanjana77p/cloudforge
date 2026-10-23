
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="CloudForge",
    description=(
        "A self-service developer platform with security "
        "and cost guardrails."
    ),
    version="0.2.0",
)

# DEMO ESTIMATES ONLY — NOT LIVE AWS PRICING.
# Replace these assumptions with verified pricing data before
# using estimates for real deployment decisions.
INSTANCE_MONTHLY_ESTIMATES_USD = {
    "small": 3.00,
    "medium": 8.00,
}

ENVIRONMENT_MULTIPLIERS = {
    "dev": 1.0,
    "staging": 1.5,
    "prod": 2.5,
}


class EnvironmentRequest(BaseModel):
    environment: Literal["dev", "staging", "prod"]

    aws_region: Literal[
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "ap-south-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "eu-west-1",
        "eu-central-1",
    ] = "us-east-1"

    application_name: str = Field(
        default="sample-app",
        min_length=2,
        max_length=30,
        pattern=r"^[a-z][a-z0-9-]*$",
    )

    instance_size: Literal["small", "medium"] = "small"

    monthly_budget_usd: float = Field(
        default=5.0,
        gt=0,
        le=5.0,
    )


def estimate_monthly_cost(
    environment: str,
    instance_size: str,
) -> float:
    """Return an illustrative estimate using demo assumptions."""
    base_cost = INSTANCE_MONTHLY_ESTIMATES_USD[instance_size]
    multiplier = ENVIRONMENT_MULTIPLIERS[environment]

    return round(base_cost * multiplier, 2)


def build_cost_estimate(request: EnvironmentRequest) -> dict:
    estimated_cost = estimate_monthly_cost(
        request.environment,
        request.instance_size,
    )
    budget_exceeded = estimated_cost > request.monthly_budget_usd

    return {
        "environment": request.environment,
        "instance_size": request.instance_size,
        "monthly_budget_usd": request.monthly_budget_usd,
        "estimated_monthly_cost_usd": estimated_cost,
        "budget_status": (
            "over_budget" if budget_exceeded else "within_budget"
        ),
        "budget_exceeded": budget_exceeded,
        "remaining_budget_usd": round(
            request.monthly_budget_usd - estimated_cost, 2
        ),
        "estimate_type": "illustrative_demo_estimate",
        "pricing_source": None,
        "message": (
            "Illustrative estimate only. These values are demo "
            "assumptions, not verified AWS prices. This estimate "
            "does not include all AWS services, usage, taxes, or "
            "regional pricing differences."
        ),
    }


@app.get("/")
def home():
    return {
        "project": "CloudForge",
        "message": "Welcome to your self-service developer platform!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/platform")
def platform_info():
    return {
        "name": "CloudForge",
        "version": "0.2.0",
        "environment": "local",
        "features": [
            "Infrastructure as Code",
            "Environment planning",
            "Illustrative cost estimation",
            "Budget threshold validation",
            "Security guardrails",
        ],
    }


@app.post("/cost/estimate")
def cost_estimate(request: EnvironmentRequest):
    """Estimate illustrative monthly cost without provisioning resources."""
    return build_cost_estimate(request)


@app.post("/environments/plan")
def plan_environment(request: EnvironmentRequest):
    estimate = build_cost_estimate(request)

    return {
        "project": "CloudForge",
        "application_name": request.application_name,
        "aws_region": request.aws_region,
        "status": "plan_created",
        "provisioning": False,
        "message": (
            "Plan created successfully. No AWS resources were created."
        ),
        **estimate,
    }
