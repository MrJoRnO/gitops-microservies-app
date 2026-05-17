# saas-api-gateway — App Repo

Flask microservice serving as the API gateway for the cloud-native SaaS platform.  
CI/CD via GitHub Actions → ECR → ArgoCD (GitOps).

---

## Repository Structure

```
app-repo/
├── src/
│   └── main.py              # Flask application
├── tests/
│   └── test_main.py         # pytest tests
├── .github/
│   └── workflows/
│       ├── ci.yml           # Lint + test (every push / PR)
│       └── cd.yml           # Build → Trivy scan → ECR push → GitOps update
├── Dockerfile
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Dev/test dependencies (not in Docker image)
└── README.md
```

---

## GitOps Flow

```
push to app-repo branch
        │
        ▼
  CI: lint + test
        │
        ▼ (only on dev / staging / main)
  CD: docker build
        │
        ▼
  Trivy scan (blocks on CRITICAL)
        │
        ▼
  Push to ECR
  tag: <branch>-<short-sha>
        │
        ▼
  Clone config-repo (<branch>)
  kustomize edit set image → overlay/<env>/kustomization.yaml
  git push config-repo
        │
        ▼
  ArgoCD detects change → auto-sync → cluster updated
```

### Branch → Environment Mapping

| App-repo branch | Config-repo branch | Overlay | Cluster |
|---|---|---|---|
| `dev` | `dev` | `staging` | dev |
| `staging` | `staging` | `staging` | staging |
| `main` | `main` | `production` | production |

---

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linter
ruff check src/ tests/

# Run app locally
python src/main.py
# → http://localhost:9898
```

---

## GitHub Actions Secrets Required

| Secret | Description |
|---|---|
| `AWS_CI_ROLE_ARN` | ARN of the IAM role for OIDC auth (no static keys) |
| `GHA_PAT` | GitHub Personal Access Token with `repo` scope (to push config-repo) |

The IAM role (`AWS_CI_ROLE_ARN`) is created by Terraform in the config-repo  
(`infra/terraform/modules/iam/github_oidc.tf`).

---

## Endpoints

| Path | Method | Description |
|---|---|---|
| `/` | GET | Returns env name and version |
| `/healthz` | GET | Liveness probe |
| `/readyz` | GET | Readiness probe |
