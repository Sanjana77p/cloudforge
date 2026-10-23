# CloudForge — Self-Service Developer Platform

CloudForge is a portfolio project exploring how platform engineering teams can simplify environment requests through API-driven workflows, Infrastructure as Code (IaC), automated testing, security scanning, and cost-aware guardrails.

The current MVP includes a FastAPI environment-planning API, a reusable Terraform module that defines secure S3 storage, automated validation and tests, and a GitHub Actions CI pipeline. AWS deployment, live cost estimation, and automated billing controls are not yet implemented.

## Architecture

```text
Developer
    |
    v
FastAPI Environment Planning API
    |
    +--> Request validation
    +--> Environment plan response
    +--> Health and platform endpoints
    |
    v
Terraform Configuration
    |
    +--> Reusable application environment module
    +--> S3 storage configuration
    +--> Public-access blocking
    +--> SSE-S3 encryption and versioning
    +--> Lifecycle policies and outputs
    |
    v
GitHub Actions CI
    |
    +--> Python API tests
    +--> Terraform formatting and validation
    +--> Terraform tests with mocked AWS provider
    +--> Checkov security scanning
```

The CI workflow validates and tests the project without AWS credentials. It does not deploy resources or run a Terraform plan against AWS.

## Implemented Features

### API and request validation

- FastAPI endpoints for health checks, platform information, and environment planning.
- Input validation for environment, AWS region, application name, instance size, and monthly budget.
- Automated pytest coverage for valid requests and invalid inputs.
- Interactive API documentation through Swagger UI.

### Infrastructure as Code

- Terraform provider and version constraints.
- Validated input variables and default resource tags.
- Reusable application environment module.
- S3 bucket configuration with a generated name prefix.
- S3 Block Public Access configuration.
- Server-side encryption using SSE-S3 (AES256).
- S3 versioning enabled.
- Lifecycle rules to expire noncurrent object versions after 30 days and abort incomplete multipart uploads after 7 days.
- Terraform outputs for the S3 bucket name and ARN.

### Testing and security

- Python API tests using pytest.
- Terraform formatting, validation, and automated tests.
- Mocked AWS provider for credential-free Terraform tests.
- Checkov static security scanning in CI.
- GitHub Actions workflows triggered by pushes to `main` and pull requests targeting `main`.

### Security decisions

The current Checkov scan reports 13 passed checks, 0 failed checks, and 4 skipped checks.

The skipped checks are documented exceptions for the following controls:

| Check | Current decision |
|---|---|
| CKV_AWS_18 | S3 access logging deferred |
| CKV_AWS_144 | Cross-region replication deferred |
| CKV2_AWS_62 | S3 event notifications deferred |
| CKV_AWS_145 | KMS encryption deferred; SSE-S3 (AES256) is used |

These exceptions are intentional MVP scope decisions, not implemented controls. Reassess them against security, audit, disaster recovery, and compliance requirements before production use.

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
- PowerShell on Windows, or a compatible terminal

AWS credentials are not required to run the API tests, Terraform validation, Terraform tests with the mocked provider, or the CI security scan.

## Run Locally

Clone the repository:

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

The API validates the request and returns a planning response. It does not create AWS resources, enforce actual AWS spending, or guarantee that the requested configuration can be deployed within the requested budget.

## Run API Tests

From the repository root:

```powershell
python -m pytest -v
```

## Validate and Test Terraform

Run these commands from the repository root:

```powershell
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform test
```

The Terraform tests use a mocked AWS provider, allowing configuration tests to run without AWS credentials.

## Run Checkov

If Checkov is installed in your active Python environment:

```powershell
checkov -d terraform --framework terraform
```

The scan includes documented exceptions for four deferred controls. A skipped check should not be interpreted as proof that the corresponding control is implemented.

## Cost and Deployment Considerations

- The API's monthly budget input is a validation constraint, not an AWS billing cap.
- No successful AWS deployment has been verified for this project.
- The Terraform configuration defines an S3 bucket and associated security controls, but these resources exist only as configuration until deliberately deployed.
- S3 storage, requests, and other AWS usage can incur charges after deployment.
- Review AWS permissions, estimated costs, and required security controls before applying Terraform.
- Actual cost estimation, AWS Budgets alerts, automated provisioning, and runtime monitoring remain future enhancements.

Never commit AWS access keys, secret keys, session tokens, or other credentials to Git.

## Roadmap

- [x] FastAPI environment-planning API
- [x] API input validation and automated tests
- [x] Reusable Terraform application environment module
- [x] S3 storage configuration and security controls
- [x] Terraform automated tests
- [x] GitHub Actions CI workflow
- [x] Checkov security scanning in CI
- [x] Credential-free Terraform tests using provider mocking
- [ ] Infrastructure cost estimation
- [ ] AWS Budgets and billing alerts
- [ ] Reviewed, cost-controlled AWS deployment
- [ ] Approval-based provisioning workflow
- [ ] Automated deployment and runtime monitoring

## Project Status

**Local MVP implemented; AWS deployment and live FinOps automation remain future work.**

CloudForge demonstrates API development, Infrastructure as Code, automated validation, CI, and security-conscious platform engineering. Its next phase focuses on realistic cost estimation, approval-based provisioning, and safe AWS deployment.
