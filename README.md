# Cyber Portfolio Deployment

This is my Django portfolio project. I made it to learn devops and devsecops. I dont know everything yet but this is what I built so far.

It has a blog and some pages. The app runs in docker containers and I also deploy it on kubernetes using minikube.

## What is inside

The app is a Django project with these apps:

- cyber_portfolio (the main settings and urls)
- blog
- identity
- tasks

It uses PostgreSQL for the database, Redis for caching, and Celery for background tasks.

## Tools I used

- Docker and docker compose
- Kubernetes (minikube)
- Nginx
- Gunicorn
- Prometheus, Grafana and cAdvisor
- Velero and MinIO
- GitHub Actions
- Bandit

## Running with docker compose

First copy the env file:

```bash
cp .env.example .env
```

Then set your passwords inside .env. After that run:

```bash
docker compose up -d --build
```

There is also a small script that does this for me:

```bash
./run.sh dev
```

or

```bash
./run.sh prod
```

The compose file has these services:

- web (django + gunicorn)
- nginx (reverse proxy, the only port open to the internet)
- db (postgres 15)
- redis (cache)
- celery (background tasks)

The backend network is internal so postgres and redis are not reachable from the internet.

## Monitoring

I added a monitoring stack. Run it together with the project:

```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

This starts prometheus, cadvisor and grafana. Prometheus reads the metrics every 15 seconds. Grafana has a dashboard and you open it on port 3000.

## Kubernetes deployment

All the kubernetes files are in the k8s folder. I run everything in the cyber-prod-env namespace.

There is a script that applies everything in the right order:

```bash
chmod +x scripts/K8s-Deploy.sh
./scripts/K8s-Deploy.sh
```

The script creates the namespace, applies the network policies, configmaps and secrets, sets up storage, deploys postgres as a StatefulSet, then redis, django (2 replicas) and celery. It also applies the ingress and the monitoring.

The django image is built locally and loaded into minikube, that is why imagePullPolicy is Never.

## Security stuff I tried to do

- Multi stage docker build so the final image is smaller
- The app runs as a non root user (a user named ali)
- Bandit scans the python code during the build and in CI/CD
- Network policies so only django and celery can reach postgres and redis
- Passwords are in kubernetes secrets, not written inside the yaml files
- .env files are in gitignore so the secrets are not pushed to github
- A restricted RBAC role for the developers
- Healthchecks on postgres, redis, django and celery

## CI/CD

There is a github actions workflow in .github/workflows/ci-cd.yml. It runs when I push or make a pull request to main.

It has 3 jobs:

1. Security scan with bandit
2. Run the django tests (with a postgres container)
3. Build and push the image to docker hub

Trivy was in the workflow before but I commented it out because I had a problem with it.

## Backup

I use velero for the backups. The backups go to MinIO which runs in the velero namespace.

There is a daily schedule that runs at 2 AM and keeps the backup for 7 days.

I can also make a backup manually:

```bash
./scripts/backup.sh
```

## Things I still want to fix

- The redis readiness probe uses POSTGRES_PASSWORD instead of REDIS_PASSWORD, I know about it and I will fix it
- The HPA file is ready but it is not applied yet
- I should rotate the .env credentials

This project is not perfect but I learned a lot while building it and I keep improving it.
