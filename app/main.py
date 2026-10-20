
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="CloudForge",
    description="A self-service developer platform with security and cost guardrails.",
    version="0.1.0",
)



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




@app.post("/environments/plan")
def plan_environment(request: EnvironmentRequest):
    return {
        "project": "CloudForge",
        "environment": request.environment,
        "application_name": request.application_name,
        "aws_region": request.aws_region,
        "instance_size": request.instance_size,
        "monthly_budget_usd": request.monthly_budget_usd,
        "status": "plan_created",
        "provisioning": False,
        "message": "Plan created successfully. No AWS resources were created.",
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
        "version": "0.1.0",
        "environment": "local",
        "features": [
            "Infrastructure as Code",
            "Automated deployments",
            "Security guardrails",
            "Cost estimation",
        ],
    }
