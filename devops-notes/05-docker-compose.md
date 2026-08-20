# Docker Compose

## docker-compose.yml

5 services total:

- `web` - Django + Gunicorn on port 8000 (built from Dockerfile)
- `nginx` - reverse proxy on port 80 (the only one exposed to host)
- `db` - PostgreSQL 15 on port 5432
- `redis` - Redis 7 on port 6379
- `celery` - background worker (built from Dockerfile.celery)

## Networks

Two networks: `frontend_net` connects nginx and web, `backend_net` connects everything else. The backend network is set to `internal: true` so those containers can't reach the internet.

## Volumes

`postgres_data` and `redis_data` for persistence.

## Dependencies

Web waits for db and redis to be healthy. Celery waits for web. Nginx waits for web.

## docker-compose.monitoring.yml

Separate file with 3 more services:
- `prometheus` on port 9090
- `cadvisor` on port 8080
- `grafana` on port 3000

Start with `docker compose -f docker-compose.monitoring.yml up -d`

## Common commands

```
docker compose up -d --build        # start everything
docker compose down                  # stop everything
docker compose logs -f web          # watch web logs
docker compose ps                    # see what's running
docker compose exec web bash        # jump into the container
docker compose restart web          # restart one service
```
