
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="CloudForge",
    description="A self-service developer platform with security and cost guardrails.",
    version="0.1.0",
)


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
