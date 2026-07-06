#!/usr/bin/env bash



# Load shared functions
source "$(dirname "$0")/common.sh"

log_info "Starting diagnosis..."


# Check cluster connection
check_cluster


log_info "Checking pods..."



# Show all pods
kubectl get pods -n "$NAMESPACE"

echo



# Show recent events
log_info "Checking events..."

kubectl get events \
-n "$NAMESPACE" \
--field-selector type=Warning \
--sort-by=.metadata.creationTimestamp | tail -5




# Find the first pod that is not Running
POD=$(kubectl get pods -n "$NAMESPACE" \
--field-selector=status.phase!=Running \

--no-headers 2>/dev/null | awk '{print $1}' | head -1)




# If a failed pod exists
if [ -n "$POD" ]; then

    log_warn "Problem found in pod: $POD"

    echo
    log_info "Pod details..."
    kubectl describe pod "$POD" -n "$NAMESPACE"


    echo
    log_info "Pod logs..."
    kubectl logs "$POD" -n "$NAMESPACE" --tail=30

else
    log_success "All pods are running."

fi


log_success "Diagnosis completed."
