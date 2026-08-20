# Kubernetes

Everything is in `k8s/` and runs in the `cyber-prod-env` namespace.

## What's in there

**Namespace** - `k8s/namespace.yaml` creates `cyber-prod-env`

**Secrets** - `k8s/secrets.yaml` has placeholder creds for DB, Django, Redis, MinIO. All `changeme_*` right now.

**ConfigMap** - `k8s/configmap.yaml` has hostnames, ports, Django settings module, MinIO endpoint.

**PostgreSQL** - There are two options:
- `postgres-statefulset.yaml` (recommended) - uses PVC so data survives restarts
- `postgres-deployment.yaml` (old) - uses emptyDir, data gets lost

**Redis** - `redis-deployment.yaml`, 1 replica with password auth.

**Django** - `django-deployment.yaml` has two deployments in one file:
- `django-web` with 2 replicas, runs as non-root, has liveness/readiness probes
- `celery-worker` with 1 replica

**Services** - ClusterIP services for django (8000), celery (8000), postgres (5432), redis (6379)

**Ingress** - Routes `ali-devsecops.local` to django-service:8000

**Network Policies** - Only django-web and celery-worker can reach postgres and redis

**RBAC** - Developer role for `ahmed-developer` that can read most things and update deployments

**HPA** - Configured for 2-5 replicas at 60% CPU but not applied yet

**PodMonitor** - Scrapes django-web pods every 15s for metrics

**Velero + MinIO** - Daily backups at 2AM, keeps 7 days

## Deploy script

`scripts/K8s-Deploy.sh` applies everything in order: namespace, RBAC, network policies, config/secrets, storage, postgres, redis, django+celery, ingress, monitoring, velero.

## Useful commands

```
kubectl get pods -n cyber-prod-env
kubectl logs -f deployment/django-web -n cyber-prod-env
kubectl exec -it deployment/django-web -n cyber-prod-env -- bash
kubectl get events -n cyber-prod-env --sort-by='.lastTimestamp'
kubectl scale deployment django-web --replicas=3 -n cyber-prod-env
```

## Known bugs

The Redis readiness probe uses `POSTGRES_PASSWORD` instead of `REDIS_PASSWORD` - that's a bug. Also Celery hardcodes `DB_HOST` and `DB_PORT` instead of using the ConfigMap.
