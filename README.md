
# CloudForge

CloudForge is a self-service developer platform prototype designed to
explore automated cloud provisioning, deployment workflows, security
guardrails, and cost estimation on AWS.

## Current features

- Python API built with FastAPI
- Health-check endpoint
- Platform information endpoint
- Interactive API documentation
- Automated endpoint tests using pytest

## Technology stack

- AWS (planned deployment platform)
- Python
- FastAPI
- Uvicorn
- pytest
- Terraform (planned infrastructure as code)
- Git and GitHub

## Local setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install "fastapi[standard]" pytest httpx
```

### 3. Run the application

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 4. Open the API documentation

http://127.0.0.1:8000/docs

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Roadmap

- [x] Initial API and health check
- [x] Automated endpoint tests
- [ ] Terraform infrastructure
- [ ] CI/CD with GitHub Actions
- [ ] Security scanning
- [ ] Infrastructure cost estimation
- [ ] AWS deployment with least-privilege access

## Project status

Early development. AWS infrastructure has not yet been provisioned.
