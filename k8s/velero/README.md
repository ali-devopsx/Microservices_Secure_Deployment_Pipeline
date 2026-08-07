# Kubernetes Backup Setup

This update adds better storage for PostgreSQL and backup support

## PostgreSQL StatefulSet

Changed PostgreSQL from Deployment to StatefulSet

Why?

* Keep PostgreSQL data safe.
* Keep the Pod name stable.
* Use persistent storage with volumeClaimTemplates

File:


k8s/postgres-statefulset.yaml


---

## MinIO for Backup

Added MinIO to store Velero backups

File:


k8s/velero/minio-setup.yaml


It creates

* Velero namespace
* MinIO Deployment
* MinIO Service

---

## Velero Schedule

Added a daily backup schedule

File:


k8s/velero/velero-schedule.yaml


Backup runs every day at 2:00 AM and keeps the backup for 7 day

---

## Deploy Script

Added one script to apply all changes

File:


scripts/deploy-advanced.sh


Run:

chmod +x scripts/deploy-advanced.sh
./scripts/deploy-advanced.sh


The script:

1. Removes the old PostgreSQL Deployment
2. Creates the new StatefulSet
3. Sets up MinIO
4. Creates the Velero backup schedule



## Infrastructure After Update


Kubernetes

|- microservices-cyber-prod-env
|   ├- Application
│   └-- PostgreSQL
|       ├-- StatefulSet
|       └-- Persistent Storage
|
|- velero
    ├-- MinIO
    └-- Velero Backup


# Backup Flow


PostgreSQL
    ↓
  Velero
    ↓
  MinIO
    ↓
  Backup

