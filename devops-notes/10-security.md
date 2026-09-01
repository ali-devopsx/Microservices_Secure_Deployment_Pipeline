# 10 - Security

## What is good

### Container security

* Multi-stage Docker builds (smaller attack surface)
* Non-root user `ali` (UID 8888) in both Dockerfiles
* `runAsNonRoot: true` in K8s deployment
* `allowPrivilegeEscalation: false` in K8s deployment

### Network security

* Docker Compose: `backend_net` is `internal: true` (no internet access)
* Kubernetes: Network policies restrict pod-to-pod traffic
* Only nginx/ingress is exposed to the outside
* Nginx has rate limiting (10 r/s per IP) and security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection) added in `nginx/default.conf`

### Code security

* Bandit scan runs during Docker build (fails on HIGH severity)
* Bandit scan runs in CI/CD (push/PR to main)
* Trivy scans Docker image for vulnerabilities
* Trivy scan runs in CI/CD (push/PR + nightly)
* Removed the `/demo-sqli/` endpoint (SQL injection demo) from `app/cyber_portfolio/urls.py`

### Access control

* K8s RBAC with least-privilege for developers
* `.env` files are gitignored
* `secret_grafana.txt` is gitignored

## Issues found

### Issue 1: Secrets in code

The K8s `secrets.yaml` has placeholder passwords (`changeme_*`). These are not real secrets, but the pattern is wrong for production.

**Recommendation:** Use a secrets manager (Sealed Secrets, External Secrets, or cloud provider secrets).

### Issue 2: Grafana password in plaintext

The Grafana admin password is in `docker-compose.monitoring.yml` and `secret_grafana.txt`.

**Recommendation:** Use Docker secrets or environment variable from a secure source.

### Issue 3: Redis readiness probe uses wrong variable

In `k8s/redis-deployment.yaml`:

```yaml
exec:
  command: ["redis-cli", "-a", "$(POSTGRES_PASSWORD)", "ping"]
```

Uses `POSTGRES_PASSWORD` instead of `REDIS_PASSWORD`.

**Recommendation:** Change to `REDIS_PASSWORD`.

### Issue 4: Celery used to hardcode DB config (FIXED)

The celery container used to hardcode `DB_HOST: "postgres-service"` and `DB_PORT: "5432"`.

**Fixed:** It now reads `DB_HOST`, `DB_PORT`, `REDIS_HOST`, `REDIS_PORT` from the ConfigMap (`cyber-app-config`) using `configMapKeyRef`, same as the web container.

### Issue 5: DEBUG fallback in settings.py (PARTIALLY FIXED)

`app/cyber_portfolio/settings.py` has:

```python
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("true", "1", "yes")
```

`DJANGO_SECRET_KEY` used to fall back to a hardcoded key.

**Fixed:** `SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]` now crashes if the key is missing. No fallback anymore.

**Still open:** `DEBUG` still defaults to `True` if `DJANGO_DEBUG` is not set. Should default to `False` in production.

### Issue 6: Trivy scan does not fail build

In `security-scan.yml`, Trivy uses `exit-code: "0"`. This means the build passes even if CRITICAL vulnerabilities are found.

**Recommendation:** Set `exit-code: "1"` for CRITICAL/HIGH severity.

### Issue 7: No image scanning before deployment

The deploy workflow does not wait for the security scan to pass.

**Recommendation:** Add `needs: [security-scan]` in deploy.yml.

## Exposed ports

| Port | Service      | Exposed to host? |
|------|-------------|-----------------|
| 80   | Nginx       | Yes (Docker)    |
| 8000 | Django      | No              |
| 5432 | PostgreSQL  | No              |
| 6379 | Redis       | No              |
| 9090 | Prometheus  | Yes (monitoring)|
| 3000 | Grafana     | Yes (monitoring)|
| 8080 | cAdvisor    | Yes (monitoring)|

In Kubernetes, only the Ingress exposes traffic externally.

## Security checklist

* [x] Non-root containers
* [x] Multi-stage builds
* [x] Network policies
* [x] RBAC
* [x] Bandit code scan
* [x] Trivy image scan
* [x] Health checks
* [x] Secrets gitignored
* [ ] Real secrets management (not placeholder passwords)
* [ ] Image signing
* [ ] Pod Security Standards
* [ ] Centralized logging
