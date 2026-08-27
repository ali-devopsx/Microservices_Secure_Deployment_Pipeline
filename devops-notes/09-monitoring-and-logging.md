# Monitoring and Logging

## The monitoring stack

Prometheus collects metrics, cAdvisor gives container-level metrics (CPU, memory, network), and Grafana is where I visualize everything.

All 3 run from `docker-compose.monitoring.yml`.

## Prometheus config

In `monitoring/prometheus.yml`. Scrapes every 15 seconds:
- itself on localhost:9090
- cadvisor on cadvisor:8080
- postgres exporter on db:9187
- redis exporter on redis:9121

## Grafana

Auto-provisioned with Prometheus as the default datasource. Admin password is in `docker-compose.monitoring.yml`. Access at http://localhost:3000.

## Kubernetes monitoring

There's a PodMonitor in `k8s/django-monitor.yaml` that scrapes django-web pods. Works with Prometheus Operator if its installed in the cluster.

## Health checks

- Django: `curl http://localhost:8000/health/`
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`
- Celery: `celery inspect ping`

In K8s there are liveness and readiness probes on the Django pods.

## Logging

No centralized logging setup. I just check logs with `docker compose logs -f` or `kubectl logs -f`.

## What's missing

No ELK or Loki for centralized logging. No pre-built Grafana dashboards for Django. No Prometheus metrics exported from the app itself. No alerting with Alertmanager. Should probably add these eventually.
