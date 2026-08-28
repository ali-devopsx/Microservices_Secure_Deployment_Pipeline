# Deployment

## Two ways to deploy

### Docker Compose (local)

```
git clone https://github.com/ali-devopsx/Microservices_Secure_Deployment_Pipeline.git
cd Microservices_Secure_Deployment_Pipeline
./run.sh
```

The `run.sh` copies the right `.env` file, stops old containers, builds new ones and starts everything. Nginx on port 80, visit http://localhost and you're good.

### Kubernetes

```
minikube start
./scripts/K8s-Deploy.sh
echo "$(minikube ip) ali-devsecops.local" | sudo tee -a /etc/hosts
```

The deploy script applies everything in the right order. After that the app is at http://ali-devsecops.local.

## CI/CD deployment

Just push to main. GitHub Actions runs tests, scans for security issues, builds the image, pushes to Docker Hub, and deploys to K8s on the self-hosted runner.

## Backups

Manual: `./scripts/backup.sh` runs pg_dump from the postgres pod.

Automatic: Velero takes daily backups at 2AM.

## Rollback

No automated rollback. If something breaks:

```
kubectl rollout undo deployment/django-web -n cyber-prod-env
```

## What could be better

No staging environment, no automated rollback in CI/CD, no blue-green or canary deployments. The deploy workflow only applies the django deployment yaml, not all the K8s resources.
