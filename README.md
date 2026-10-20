# CloudForge — Self-Service Developer Platform

CloudForge is a portfolio project exploring how platform engineering teams can simplify environment requests using API-driven workflows, Infrastructure as Code, automated testing, security scanning, and cost-aware guardrails.

The current version provides a local FastAPI environment-planning API and a Terraform configuration with reusable modules and automated validation. **It does not provision AWS resources yet.**

## Architecture

```text
Developer
    |
    v
FastAPI Environment Planning API
    |
    +--> Input validation
    +--> Environment plan response
    +--> Health and platform endpoints
    |
    v
Terraform Configuration
    |
    +--> Reusable application environment module
    +--> Input validation and outputs
    +--> Terraform automated tests
    |
    v
GitHub Actions CI
    |
    +--> Python API tests
    +--> Terraform validation and tests
    +--> Terraform plan validation
    +--> Checkov security scanning
```

## Implemented Features

- **FastAPI:** API endpoints for health checks, platform information, and environment planning.
- **Input validation:** Validates environment, AWS region, application name, instance size, and requested monthly budget.
- **Automated API tests:** pytest tests covering successful requests and invalid inputs.
- **Terraform:** Version constraints, validated input variables, provider configuration, default tags, and outputs.
- **Reusable Terraform module:** Application environment naming, common tags, and validated configuration inputs.
- **Terraform tests:** Automated tests for default values, invalid inputs, and module outputs.
- **GitHub Actions:** Automated API tests, Terraform validation, Terraform tests, plan validation, and Checkov scanning.

## Technology Stack

- Python 3.12
- FastAPI and Uvicorn
- pytest and HTTPX
- Terraform
- AWS provider for Terraform
- Checkov
- Git and GitHub
- GitHub Actions

## Prerequisites

- Python 3.12 or compatible version
- Git
- Terraform CLI
- PowerShell on Windows

## Run Locally

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/Sanjana77p/cloudforge.git
cd cloudforge
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Platform information: http://127.0.0.1:8000/platform

## Example Environment Planning Request

Use Swagger UI or send this request from another PowerShell window:

```powershell
$body = @{
    environment = "dev"
    aws_region = "us-east-1"
    application_name = "sample-app"
    instance_size = "small"
    monthly_budget_usd = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/environments/plan" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

The API returns a validated plan. It does **not** create AWS resources, enforce actual AWS spending, or guarantee that the requested configuration can be deployed within the specified budget.

## Run API Tests

```powershell
python -m pytest -v
```

## Validate Terraform

Run these commands from the repository root:

```powershell
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform test
terraform -chdir=terraform plan -input=false -lock=false
```

The current Terraform configuration defines variables, module outputs, and provider settings, but no deployable AWS resources.

## Security and Cost Considerations

- Checkov scans the Terraform configuration in local development and CI.
- Terraform and API tests validate the implemented configuration and request rules.
- No AWS infrastructure is currently provisioned by this project.
- The requested monthly budget is a validation constraint, not a live billing limit.
- Actual AWS cost estimation, billing alerts, deployment permissions, and runtime security controls remain future enhancements.
- Never commit AWS access keys, secret keys, tokens, or other credentials to Git.

## Roadmap

- [x] FastAPI environment planning API
- [x] API input validation and automated tests
- [x] Terraform configuration and reusable module
- [x] Terraform automated tests
- [x] GitHub Actions CI workflow
- [x] Checkov security scanning in CI
- [x] Terraform plan validation in CI
- [ ] Infrastructure cost estimation
- [ ] AWS budget and billing alerts
- [ ] Reviewed, cost-controlled AWS deployment
- [ ] Automated deployment and runtime monitoring

## Project Status

**Working local MVP — AWS deployment not yet implemented.**

This project is being developed incrementally to demonstrate API development, Infrastructure as Code, automated validation, CI, and security-conscious platform engineering.
