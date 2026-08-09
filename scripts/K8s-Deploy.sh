#!/bin/bash

# Stop n fails
set -e

# Configuration variables
NAMESPACE="cyber-prod-env"
K8S_DIR="../k8s"

echo "=== Starting Project Deployment ==="

# Ensure Namespace exists
echo "-> Creating Namespace and RBAC"
kubectl apply -f $K8S_DIR/namespace.yaml
kubectl apply -f $K8S_DIR/developer-rbac.yaml
kubectl apply -f $K8S_DIR/network-policy.yaml
kubectl apply -f $K8S_DIR/redis-net-policy.yaml

# Configs & Secrets
echo "-> Applying ConfigMaps and Secrets"
kubectl apply -f $K8S_DIR/configmap.yaml
kubectl apply -f $K8S_DIR/secrets.yaml

# Storage
echo "-> Setting up Storage"
kubectl apply -f $K8S_DIR/media-storage.yaml

# 4. Databases (Migration from Deployment to StatefulSet)
echo "-> Deploying Databases (Postgres & Redis)"



# Delete old deployment if it exists to avoid collision
if kubectl get deployment postgres-deployment -n $NAMESPACE &> /dev/null; then
    echo "delete old postgress deployment"
    kubectl delete deployment postgres-deployment -n $NAMESPACE
fi

kubectl apply -f $K8S_DIR/postgres-statefulset.yaml

kubectl apply -f $K8S_DIR/redis-deployment.yaml



# Wait for Postgres to be ready
echo "Waiting for Postgres StatefulSet to be ready..."
kubectl rollout status statefulset/postgres -n $NAMESPACE --timeout=120s





# Core Application [Django & Celery)
echo "--> Deploying Django Application..."
kubectl apply -f $K8S_DIR/django-deployment.yaml
#kubectl apply -f $K8S_DIR/django-hpa.yaml


echo "Waiting for Django pods..."
kubectl rollout status deployment/django-deployment -n $NAMESPACE --timeout=120s



# ingress and Monitoring
echo "--> Applying Ingress and Monitoring..."
kubectl apply -f $K8S_DIR/django-ingress.yaml

if kubectl get crd podmonitors.monitoring.coreos.com &> /dev/null; then
    kubectl apply -f $K8S_DIR/django-monitor.yaml
fi


# auto-detect velero / Disaster Recovery

if [ -d "$K8S_DIR/velero" ]; then
    echo "-> Setting up Backup infrastructure..."
    kubectl apply -f $K8S_DIR/velero/minio-setup.yaml
    
    if kubectl get crd schedules.velero.io &> /dev/null; then
        kubectl apply -f $K8S_DIR/velero/velero-schedule.yaml
    fi
fi


echo " Deployment Finished Successfully!"

# Display running pods
kubectl get pods,svc -n $NAMESPACE
