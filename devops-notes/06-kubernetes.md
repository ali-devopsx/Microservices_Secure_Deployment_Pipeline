# 06 - Kubernetes

All Kubernetes files are in the `k8s/` folder.

Everything runs inside the `cyber-prod-env` namespace.

## Namespace

File: `k8s/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cyber-prod-env
```

All resources are created in this namespace.

## Secrets

File: `k8s/secrets.yaml`

Contains placeholder credentials:

* `DB_NAME`, `DB_USER`, `DB_PASSWORD`
* `DJANGO_SECRET_KEY`
* `REDIS_PASSWORD`
* `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`

**Issue:** All passwords are `changeme_*` placeholders. In production, use a real secrets manager.

## ConfigMap

File: `k8s/configmap.yaml`

Contains non-sensitive config:

* `DB_HOST`: `postgres-service`
* `DB_PORT`: `5432`
* `REDIS_HOST`: `redis-service`
* `REDIS_PORT`: `6379`
* `DJANGO_SETTINGS_MODULE`: `cyber_portfolio.settings`
* `MINIO_ENDPOINT`: `minio-service.velero.svc.cluster.local:9000`

## PostgreSQL

### StatefulSet (recommended)

File: `k8s/postgres-statefulset.yaml`

* Image: `postgres:15-alpine`
* PVC: 1Gi (`postgres-storage`) for data
* Health check: `pg_isready`
* Runs in `cyber-prod-env` namespace

### Deployment (old, alternative)

File: `k8s/postgres-deployment.yaml`

* Same image but uses Deployment instead of StatefulSet
* Uses `emptyDir` instead of PVC (data is lost on restart)

**Use StatefulSet for databases.** It keeps data stable across pod restarts.

## Redis

File: `k8s/redis-deployment.yaml`

* Image: `redis:7-alpine`
* 1 replica
* Password auth using secret

**Issue:** The readiness probe uses `POSTGRES_PASSWORD` instead of `REDIS_PASSWORD`:

```yaml
exec:
  command: ["redis-cli", "-a", "$(POSTGRES_PASSWORD)", "ping"]
```

This is wrong. Should be `REDIS_PASSWORD`.

## Django

File: `k8s/django-deployment.yaml`

This file has two deployments in one file:

### django-web

* 2 replicas
* Image: `alidevopsx/cyber-portfolio:latest`
* Port: 8000
* `runAsNonRoot: true`
* `allowPrivilegeEscalation: false`
* Health checks: liveness + readiness on `/health/`
* Reads from ConfigMap and Secrets

### celery-worker

* 1 replica
* Same image as django
* Command: `celery -A cyber_portfolio worker --loglevel=info`
* Reads DB_HOST, DB_PORT, REDIS_HOST, REDIS_PORT from the ConfigMap (`cyber-app-config`) via `configMapKeyRef`
* No more hardcoded host/port values (used to be `postgres-service` / `redis-service` written directly)

## Services

| Service           | Type     | Port | Target       |
|-------------------|----------|------|-------------|
| `django-service`  | ClusterIP | 8000 | django-web  |
| `celery-service`  | ClusterIP | 8000 | celery-worker |
| `postgres-service`| ClusterIP | 5432 | postgres    |
| `redis-service`   | ClusterIP | 6379 | redis       |

## Ingress

File: `k8s/django-ingress.yaml`

* Host: `ali-devsecops.local`
* Routes traffic to `django-service:8000`
* Sets `nginx.ingress.kubernetes.io/proxy-body-size: "10m"`

To use it, add to `/etc/hosts`:

```bash
echo "192.168.49.2 ali-devsecops.local" | sudo tee -a /etc/hosts
```

## Network Policies

### PostgreSQL access

File: `k8s/network-policy.yaml`

Only `django-web` and `celery-worker` can reach PostgreSQL.

### Redis access

File: `k8s/redis-net-policy.yaml`

Only `django-web` and `celery-worker` can reach Redis.

This is good security. Other pods cannot access the database or cache.

## RBAC

File: `k8s/developer-rbac.yaml`

* Role: `developer`
* Can: get, list, watch pods/services/logs; update deployments
* Binding: `ahmed-developer`

This follows least-privilege. The developer can read most things but only update deployments.

## HPA (Horizontal Pod Autoscaler)

File: `k8s/django-hpa.yaml`

* Min replicas: 2
* Max replicas: 5
* CPU target: 60%

**Status:** Not applied yet (commented out in deploy script).

## PodMonitor

File: `k8s/django-monitor.yaml`

* Scrapes `django-web` pods every 15 seconds
* Looks for label `app: django-web`

## Velero + MinIO

Files: `k8s/velero/`

### MinIO

* Runs in `velero` namespace
* For storing backups

### Velero Schedule

* Daily backup at 2AM
* Keeps backups for 7 days
* Snapshots PVs

## Deploy script

File: `scripts/K8s-Deploy.sh`

Applies resources in this order:

1. Namespace
2. RBAC
3. Network policies
4. ConfigMap + Secrets
5. Storage (PVCs)
6. PostgreSQL StatefulSet
7. Redis
8. Django + Celery
9. Ingress
10. Monitoring
11. Velero

## kubectl commands

```bash
# Apply all resources
./scripts/K8s-Deploy.sh

# Check pods
kubectl get pods -n cyber-prod-env

# Check services
kubectl get svc -n cyber-prod-env

# Check logs
kubectl logs -f deployment/django-web -n cyber-prod-env
kubectl logs -f deployment/celery-worker -n cyber-prod-env

# Enter a pod
kubectl exec -it deployment/django-web -n cyber-prod-env -- bash

# Check events
kubectl get events -n cyber-prod-env --sort-by='.lastTimestamp'

# Delete a pod (will restart)
kubectl delete pod <pod-name> -n cyber-prod-env

# Scale manually
kubectl scale deployment django-web --replicas=3 -n cyber-prod-env

# Check network policies
kubectl get networkpolicies -n cyber-prod-env

# Check HPA
kubectl get hpa -n cyber-prod-env
```
