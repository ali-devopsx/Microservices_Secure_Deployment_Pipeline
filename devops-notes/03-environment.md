# 03 - Environment

## Environment variables

The project reads all configuration from environment variables.

The Django settings file `app/cyber_portfolio/settings.py` reads configuration from environment variables:

**Database (required, no default):**

* `DB_NAME` - PostgreSQL database name
* `DB_USER` - PostgreSQL username
* `DB_PASSWORD` - PostgreSQL password
* `DB_HOST` - PostgreSQL host (default: `db` in Docker, `postgres-service` in K8s)
* `DB_PORT` - PostgreSQL port (default: `5432`)

**Django:**

* `DJANGO_SECRET_KEY` - Django secret key for sessions and tokens (**required, no default - the app crashes if it's missing**)
* `DJANGO_DEBUG` - Debug mode (`True` or `False`)
* `DJANGO_ALLOWED_HOSTS` - Allowed hostnames

**Redis/Celery:**

* `REDIS_HOST` - Redis host (default: `redis`)
* `REDIS_PORT` - Redis port (default: `6379`)
* `REDIS_PASSWORD` - Redis password

**MinIO (K8s only):**

* `MINIO_ROOT_USER` - MinIO admin username
* `MINIO_ROOT_PASSWORD` - MinIO admin password
* `MINIO_BUCKET` - Backup bucket name

## .env files

The project uses `.env` files for local Docker Compose:

* `.env.dev` - development settings
* `.env.prod` - production settings

The `run.sh` script copies the right `.env` file to `.env` before starting:

```bash
# run.sh
cp .env.dev .env   # or .env.prod
docker compose down
docker compose up -d --build
```

The `.env.example` file is a template with placeholder values:

```text
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=changeme
DJANGO_SECRET_KEY=changeme
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=changeme
```

## Kubernetes secrets

In Kubernetes, secrets are in `k8s/secrets.yaml`:

```yaml
stringData:
  DB_NAME: "cyber_portfolio_db"
  DB_USER: "cyber_portfolio_user"
  DB_PASSWORD: "changeme_db_password"
  DJANGO_SECRET_KEY: "changeme_django_secret_key"
  REDIS_PASSWORD: "changeme_redis_password"
  MINIO_ROOT_USER: "minio_admin"
  MINIO_ROOT_PASSWORD: "changeme_minio_password"
```

These are placeholder values. In a real project, I should use a secrets manager or sealed secrets.

## ConfigMap

In Kubernetes, non-sensitive config is in `k8s/configmap.yaml`:

```yaml
data:
  DB_HOST: "postgres-service"
  DB_PORT: "5432"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  DJANGO_SETTINGS_MODULE: "cyber_portfolio.settings"
  MINIO_ENDPOINT: "minio-service.velero.svc.cluster.local:9000"
```

## Things to improve

* The `.env` files were committed to GitHub at some point. They should be removed from git history.
* K8s secrets use placeholder passwords (`changeme_*`). In production, use a proper secrets manager.
* `secret_grafana.txt` contains a real password. It is gitignored now but was committed before.
