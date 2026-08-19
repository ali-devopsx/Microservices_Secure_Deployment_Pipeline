# Project Overview

So basically this is my Django portfolio site. I built it while learning DevOps and DevSecOps stuff. Its not a real production app or anything, more like a playground to practice deploying things properly.

The site has a blog, a portfolio section, and a task manager. Nothing too fancy but it works.

## The tech stack

Python 3.11 with Django, PostgreSQL for the database, Redis for caching and Celery stuff, Gunicorn as the WSGI server, and Nginx in front of everything.

For DevOps I'm using Docker, Docker Compose, Kubernetes (Minikube), GitHub Actions for CI/CD, Prometheus and Grafana for monitoring, and Bandit + Trivy for security scanning.

## How it all fits together

There are basically two ways I run this thing:

**Docker Compose (local dev)**

Just `docker compose up -d --build` and everything comes up. Nginx on port 80, Django on 8000 internally, PostgreSQL, Redis, and a Celery worker. Only nginx is exposed to the outside, everything else stays inside the docker network.

**Kubernetes (Minikube)**

I have a deploy script `./scripts/K8s-Deploy.sh` that applies everything. It runs in a namespace called `cyber-prod-env`. There's Django with 2 replicas, Celery with 1, PostgreSQL as a StatefulSet, Redis, an Ingress, network policies, RBAC, the whole deal. The app is accessible at `ali-devsecops.local`.

There's also a separate monitoring stack with Prometheus, Grafana and cAdvisor that runs with `docker compose -f docker-compose.monitoring.yml up -d`.

## Main files to know about

- `Dockerfile` - multi-stage build for the Django app
- `Dockerfile.celery` - builds the Celery worker
- `docker-compose.yml` - local environment
- `entrypoint.sh` - what runs when the container starts
- `k8s/` - all the Kubernetes manifests
- `scripts/` - deploy, backup, verify, diagnose scripts
- `.github/workflows/` - CI/CD pipelines
- `nginx/default.conf` - nginx config
- `monitoring/prometheus.yml` - prometheus scrape config
