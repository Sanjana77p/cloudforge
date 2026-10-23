
# CloudForge — Self-Service Developer Platform

CloudForge is a portfolio project exploring how platform engineering teams can simplify environment requests through API-driven workflows, Infrastructure as Code (IaC), automated testing, security scanning, and cost-aware guardrails.

The current MVP includes a FastAPI environment-planning API, an illustrative FinOps cost-estimation endpoint, a reusable Terraform module that defines secure S3 storage, automated validation and tests, and a GitHub Actions CI pipeline.

**AWS deployment, verified live AWS pricing, and automated billing controls are not yet implemented.**

## Architecture

```text
Developer
    |
    v
FastAPI Developer Platform
    |
    +--> Environment planning API
    +--> Request validation
    +--> Illustrative cost estimation
    +--> Budget status and remaining budget
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

The CI pipeline validates and tests the project without AWS credentials. It does not deploy resources or run a Terraform plan against AWS.

## Implemented Features

### 1. API and Request Validation

- FastAPI endpoints for health checks, platform information, and environment planning.
- Input validation for environment, AWS region, application name, instance size, and monthly budget.
- Support for `dev`, `staging`, and `prod` environment requests.
- Configurable application names, supported AWS regions, and instance-size options.
- Automated pytest coverage for valid requests and invalid inputs.
- Interactive API documentation through Swagger UI.

### 2. FinOps Cost Estimation

- `POST /cost/estimate` returns an illustrative monthly cost estimate.
- Compares the estimated cost against the requested monthly budget.
- Reports whether the estimate is within budget or over budget.
- Returns the estimated cost, budget status, budget-exceeded flag, and remaining budget.
- Includes automated tests for within-budget requests, over-budget requests, and invalid budget values.
- Clearly identifies estimates as illustrative demo estimates rather than verified AWS pricing.

**Important:** The estimator uses demo assumptions. It does not retrieve live AWS prices, calculate every service charge, enforce AWS spending limits, or guarantee that an actual deployment will stay within budget.

### 3. Infrastructure as Code

- Terraform provider and version constraints.
- Validated input variables and default resource tags.
- Reusable application environment module.
- S3 bucket configuration with a generated name prefix.
- S3 Block Public Access configuration.
- Server-side encryption using SSE-S3 (AES256).
- S3 versioning enabled.
- Lifecycle rules to expire noncurrent object versions after 30 days.
- Lifecycle rule to abort incomplete multipart uploads after 7 days.
- Terraform outputs for the S3 bucket name and ARN.
- `force_destroy = false` to prevent Terraform from automatically emptying the bucket when it is destroyed.

The Terraform configuration defines infrastructure but does not create AWS resources until an authorized, deliberate deployment is performed.

### 4. Testing and CI/CD

- Python API tests using pytest.
- Terraform formatting and validation.
- Terraform automated tests using a mocked AWS provider.
- Terraform configuration tests that do not require AWS credentials.
- Checkov static security scanning.
- GitHub Actions workflow triggered by pushes to `main` and pull requests targeting `main`.
- Automated validation of application code and infrastructure configuration.

The current pipeline checks configuration and security policies. Automated deployment is not part of the current workflow.

### 5. Security Decisions

The latest reported local Checkov scan showed:

- Passed checks: 13
- Failed checks: 0
- Skipped checks: 4

The four skipped checks are documented exceptions for controls deferred in this cost-conscious MVP.

| Check | Current decision |
|---|---|
| `CKV_AWS_18` | S3 access logging deferred until a dedicated logging destination is required. |
| `CKV_AWS_144` | Cross-region replication deferred until disaster-recovery requirements justify the additional cost. |
| `CKV2_AWS_62` | S3 event notifications deferred because the MVP has no event-driven S3 workflow. |
| `CKV_AWS_145` | KMS encryption deferred; SSE-S3 (AES256) is used for this MVP. |

These exceptions are documented scope decisions, not implemented controls. A skipped Checkov check does not prove that the corresponding control is configured.

Before production use, reassess these decisions against security, audit, disaster-recovery, data-retention, and compliance requirements.

## Technology Stack

- **Language:** Python 3.12
- **API:** FastAPI and Uvicorn
- **Testing:** pytest and HTTPX
- **Infrastructure as Code:** Terraform
- **Cloud provider:** AWS provider for Terraform
- **Security scanning:** Checkov
- **Version control:** Git and GitHub
- **CI:** GitHub Actions

## Prerequisites

Install the following tools:

- Python 3.12 or a compatible version
- Git
- Terraform CLI
- PowerShell on Windows, or a compatible terminal

AWS credentials are not required to run the API tests, Terraform validation, Terraform tests with provider mocking, or the CI security scan.

## Run Locally

### 1. Clone the repository

```powershell
git clone https://github.com/Sanjana77p/cloudforge.git
cd cloudforge
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can temporarily allow scripts for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

### 5. Open the API documentation

With the application running, use these local endpoints:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Platform information: http://127.0.0.1:8000/platform

## Example: Environment Planning

Use Swagger UI or send this request from another PowerShell window.

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

The API validates the request and returns an environment-planning response. It does not create AWS resources or enforce actual AWS spending.

## Example: FinOps Cost Estimation

Submit an illustrative cost-estimation request:

```powershell
$body = @{
    environment = "dev"
    aws_region = "us-east-1"
    application_name = "sample-app"
    instance_size = "small"
    monthly_budget_usd = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/cost/estimate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

The response includes fields such as:

- `estimated_monthly_cost_usd`
- `budget_status`
- `budget_exceeded`
- `remaining_budget_usd`
- `estimate_type`
- `pricing_source`

The current demo estimator returns illustrative values. It does not use a verified AWS pricing source, and its estimates must not be treated as actual deployment costs.

## Run API Tests

From the repository root, activate the virtual environment and run:

```powershell
python -m pytest -v
```

The tests cover the API endpoints, request validation, environment planning, and illustrative cost-estimation behavior.

## Validate and Test Terraform

Run the following commands from the repository root:

```powershell
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform test
```

The Terraform tests use a mocked AWS provider, allowing configuration tests to run without AWS credentials.

**Do not run `terraform apply` as part of routine validation.** Review the configuration, permissions, deployment plan, and potential charges before any real AWS deployment.

## Run Checkov

If Checkov is installed in your active Python environment:

```powershell
checkov -d terraform --framework terraform
```

Checkov scans the Terraform configuration against security policies. The current configuration documents four deferred controls using inline Checkov skip comments.

Review skipped checks periodically. Do not remove or suppress security findings without a clear, documented justification.

## Cost and Deployment Considerations

- The monthly budget field is an application-level validation input, not an AWS billing cap.
- The demo cost estimator does not retrieve live pricing or guarantee actual costs.
- No successful AWS deployment has been verified for this project.
- The Terraform configuration defines an S3 bucket and associated security controls; these resources exist only as configuration until deliberately deployed.
- S3 storage, requests, versioned objects, and other AWS usage can incur charges after deployment.
- Review IAM permissions, potential costs, security requirements, and the Terraform plan before applying infrastructure.
- AWS Budgets alerts, actual billing integration, automated provisioning, and runtime monitoring remain future enhancements.
- Never commit AWS access keys, secret keys, session tokens, or other credentials to Git.

## Roadmap

- [x] FastAPI environment-planning API
- [x] API input validation and automated tests
- [x] Reusable Terraform application environment module
- [x] S3 storage configuration and security controls
- [x] Terraform automated tests
- [x] GitHub Actions CI workflow
- [x] Checkov security scanning in CI
- [x] Credential-free Terraform tests using provider mocking
- [x] Illustrative FinOps cost-estimation endpoint and tests
- [ ] Integration with a verified AWS pricing source
- [ ] AWS Budgets and billing alerts
- [ ] Approval-based provisioning workflow
- [ ] Reviewed, cost-controlled AWS deployment
- [ ] Automated deployment and runtime monitoring

## Project Status

**Local MVP implemented; AWS deployment and live FinOps automation remain future work.**

CloudForge currently demonstrates API development, Infrastructure as Code, automated testing, CI, static security scanning, and illustrative budget guardrails.

The next phase focuses on verified cost estimation, approval-based provisioning, and safe AWS deployment with explicit permission and cost reviews.
