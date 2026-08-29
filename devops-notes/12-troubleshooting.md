# Troubleshooting

## Container won't start

Check `docker compose logs web`. Usually its a missing `.env` file or PostgreSQL not being ready yet. The `entrypoint.sh` waits for the database with netcat so give it a sec.

## Port 80 already in use

Something else is using port 80. Check with `sudo lsof -i :80` or `docker compose ps`. Stop whatever is using it.

## Database connection refused

Django can't reach PostgreSQL. Make sure `DB_HOST=db` not `localhost`. Check the password in `.env` matches what PostgreSQL expects. Make sure both containers are on the same network (`backend_net`).

## Environment variable missing

Django throws `ImproperlyConfigured`. Run `docker compose exec web env | grep DJANGO` to see what's set. Check `.env.example` for the full list.

## Kubernetes pod stuck in ImagePullBackOff

The image name is wrong or it doesn't exist on Docker Hub. Check with `kubectl describe pod <pod-name> -n cyber-prod-env`. Make sure `imagePullPolicy` is set correctly.

## Kubernetes pod in CrashLoopBackOff

Check logs: `kubectl logs <pod-name> -n cyber-prod-env`. Usually it's missing env vars, wrong DB host, or wrong password. Check that secrets and configmap are applied.

## CI/CD workflow fails

Go to the Actions tab on GitHub. Check which step failed. Common issues: test database env vars are wrong, Bandit finds security issues, Docker build fails.

## Redis connection refused

Make sure `REDIS_HOST=redis` (the service name, not localhost). Check `REDIS_PASSWORD` is correct. In K8s check the network policy allows access.

## Celery not processing tasks

Check `docker compose logs celery`. Make sure Redis is accessible and `CELERY_BROKER_URL` points to it. Try restarting: `docker compose restart celery`.

## Ingress not working

Check DNS: `grep ali-devsecops.local /etc/hosts`. Check Minikube IP: `minikube ip`. Make sure the ingress controller is running: `kubectl get pods -n ingress-nginx`.

## Diagnostic script

There's `./scripts/diagnose.sh` that lists pods, events, finds non-running pods and shows their logs. Use it when stuff breaks in K8s.
