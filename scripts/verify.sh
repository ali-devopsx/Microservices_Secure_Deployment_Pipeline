#!/usr/bin/env bash

# Load shared functions
source "$(dirname "$0")/common.sh"

log_info "Checking cluster..."

# Make sure the cluster is reachable
check_cluster

log_info "Checking deployment..."

# Wait until the deployment is ready
kubectl rollout status deployment/django-deployment \
-n "$NAMESPACE" \
--timeout=60s

log_info "Checking pods..."

# Show all pods in the namespace
kubectl get pods -n "$NAMESPACE"

log_info "Checking service..."

# Show all services
kubectl get svc -n "$NAMESPACE"

log_info "Checking application..."

# Get the HTTP status code
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)

# Check if the application is healthy
if [ "$STATUS" = "200" ]; then
    log_success "Application is healthy."
else
    log_error "Health check failed."
    exit 1
fi

log_success "Verification completed."
