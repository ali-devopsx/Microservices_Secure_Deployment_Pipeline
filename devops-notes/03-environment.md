# Environment

## How config works

Everything is driven by environment variables. The Django settings in `app/cyber_portfolio/settings.py` reads everything from `os.environ.get(...)`.

The main ones I need:

**Database:** `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

**Django:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`

**Redis/Celery:** `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`

**MinIO (K8s only):** `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `MINIO_BUCKET`

## .env files

For Docker Compose I have `.env.dev` and `.env.prod`. The `run.sh` script copies the right one to `.env` before starting everything up.

`.env.example` has placeholder values so I remember what goes where.

## Kubernetes secrets

In K8s all the credentials are in `k8s/secrets.yaml`. Right now they're all `changeme_*` placeholders which is obviously not great for production. I should look into Sealed Secrets or something similar.

## ConfigMap

Non-sensitive stuff like hostnames and ports go in `k8s/configmap.yaml`. Things like `DB_HOST: "postgres-service"`, `REDIS_HOST: "redis-service"`, etc.

## Problems

The `.env` files got committed to GitHub at some point even though they're in `.gitignore` now. Also `secret_grafana.txt` has a real password that was committed before. I should probably clean the git history at some point.
