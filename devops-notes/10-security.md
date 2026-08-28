# Security

## What I did right

- Multi-stage Docker builds (less stuff in the final image)
- Non-root user in containers (UID 8888)
- `runAsNonRoot: true` and `allowPrivilegeEscalation: false` in K8s
- Backend network is internal in Docker Compose (no internet access)
- Network policies in K8s restrict pod-to-pod traffic
- Bandit scans code during Docker build and in CI/CD
- Trivy scans the Docker image
- RBAC with least-privilege for developers
- `.env` files and secrets are gitignored

## Problems I found

**Placeholder passwords** - K8s secrets.yaml has `changeme_*` values. Need a real secrets manager for production.

**Grafana password in plaintext** - Its in docker-compose.monitoring.yml and secret_grafana.txt. Should use Docker secrets or something.

**Redis probe uses wrong variable** - In `k8s/redis-deployment.yaml` the readiness probe runs `redis-cli -a $(POSTGRES_PASSWORD) ping`. Should be `REDIS_PASSWORD`.

**Celery hardcodes DB config** - Instead of using ConfigMap it just hardcodes `DB_HOST: "postgres-service"` and `DB_PORT: "5432"`.

**DEBUG fallback** - In settings.py if `DJANGO_SECRET_KEY` is missing it falls back to a hardcoded key `"my_ultra_secret_production_key_2026"`. Should just crash instead.

**Trivy doesn't fail the build** - `exit-code: "0"` means even critical vulnerabilities pass. Should be `"1"` for production.

## Exposed ports

Only port 80 (nginx) and the monitoring ports (9090, 3000, 8080) are exposed. Everything else is internal.

## Security checklist

- [x] Non-root containers
- [x] Multi-stage builds
- [x] Network policies
- [x] RBAC
- [x] Bandit + Trivy scanning
- [x] Health checks
- [ ] Real secrets management
- [ ] Image signing
- [ ] Centralized logging
