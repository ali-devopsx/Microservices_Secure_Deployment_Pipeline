# 07 - CI/CD

The project uses GitHub Actions for CI/CD.

There are 3 workflows:

## 1. ci-cd.yml (Tests + Build)

File: `.github/workflows/ci-cd.yml`

**Trigger:** Push or PR to `main`

### Flow

```
Code Push → Tests → Build Docker Image → Push to Docker Hub
```

### Steps

1. **Checkout code**
2. **Set up Python 3.11**
3. **Run tests** with a PostgreSQL service container:
   * Creates a test database
   * Installs requirements
   * Runs `python manage.py test`
4. **Build Docker image** with Buildx
   * Tag: `alidevopsx/cyber-portfolio:latest`
   * Also tags with SHA: `alidevopsx/cyber-portfolio:<sha>`
   * Uses GitHub Actions cache
5. **Push to Docker Hub**
   * Only on `main` branch (not on PRs)

### Environment variables

* `DB_NAME`, `DB_USER`, `DB_PASSWORD` for test database
* `DJANGO_SECRET_KEY` for tests - set to a static test-only value (`ci-test-secret-key-for-testing-only`), because settings.py no longer has a default fallback

## 2. security-scan.yml (Security)

File: `.github/workflows/security-scan.yml`

**Trigger:** Push or PR to `main` + nightly at 2AM

### Flow

```
Code Push → Bandit (code scan) + Trivy (image scan)
```

### Steps

1. **Bandit scan** (code security):
   * `bandit -r app/ --severity-level high`
   * Scans Python code for security issues
   * Fails if HIGH severity issues found

2. **Trivy scan** (Docker image security):
   * Scans `alidevopsx/cyber-portfolio:latest`
   * Checks for CRITICAL and HIGH vulnerabilities
   * `exit-code: "0"` - does NOT fail the build (informational)

### .trivyignore

File: `.trivyignore`

Lists CVEs to ignore:

```text
CVE-2011-3374
CVE-2017-18018
CVE-2026-42496
CVE-2026-8376
```

## 3. deploy.yml (Deployment)

File: `.github/workflows/deploy.yml`

**Trigger:** Push to `main`

### Flow

```
Code Push → Build Image → Deploy to Kubernetes (self-hosted runner)
```

### Steps

1. **Checkout code**
2. **Build Docker image**
3. **Apply Kubernetes manifests**
   * Runs on a **self-hosted runner**
   * Applies `k8s/django-deployment.yaml`

### Important notes

* This workflow runs on a self-hosted runner, not GitHub-hosted
* The runner needs `kubectl` configured and access to the cluster
* Only applies the Django deployment (not all K8s resources)

## Full CI/CD flow

```
1. Developer pushes code to main
2. GitHub Actions runs:
   a. Tests (ci-cd.yml)
   b. Security scan (security-scan.yml)
   c. Build + Push image (ci-cd.yml)
   d. Deploy to K8s (deploy.yml)
3. Application updates on the cluster
```

## Docker Hub

The image is pushed to:

* `alidevopsx/cyber-portfolio:latest`
* `alidevopsx/cyber-portfolio:<git-sha>`

## Things to improve

* Trivy scan does not fail the build (`exit-code: "0"`). In production, it should fail on CRITICAL issues.
* The deploy workflow only applies `django-deployment.yaml`. It does not apply other K8s resources (ConfigMap, Secrets, NetworkPolicy, etc.).
* No staging environment. Changes go directly to production.
* No rollback strategy if deployment fails.
