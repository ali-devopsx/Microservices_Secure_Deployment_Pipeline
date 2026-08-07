#!/usr/bin/env bash

# Load shared functions
source "$(dirname "$0")/common.sh"



# Start backup
log_info "Starting database backup"



# Check connection
check_cluster


# Create backup Folder
mkdir -p backups

# backup FileName
BACKUP_FILE="backups/postgres-$(date +%F-%H%M).sql"



# Get Postgre pod name
POD=$(kubectl get pod -n "$NAMESPACE" \
-l app=postgres \
-o jsonpath='{.items[0].metadata.name}')



# Stop if no Postgre pod is found
if [ -z "$POD" ]; then
    log_error "Postgres pod not found."
    exit 1
fi


# Show pod name
log_info "use pod: $POD"


# Export database to SQL file
kubectl exec "$POD" -n "$NAMESPACE" -- \
pg_dump -U postgres cyber_db > "$BACKUP_FILE"

# Check backup result
if [ $? -eq 0 ]; then

    log_success "Backup completed."
    log_info "File: $BACKUP_FILE"


else
    log_error "Backup failed"
    exit 1
fi
