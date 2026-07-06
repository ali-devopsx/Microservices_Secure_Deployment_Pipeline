#!/usr/bin/env bash

set -euo pipefail



# --------------
# Global Config
# --------------
NAMESPACE="${NAMESPACE:-cyber-prod-env}"
APP_NAME="${APP_NAME:-django}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"

REPORT_DIR="${REPORT_DIR:-./reports}"




# --------
# Color
# --------
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m"


# ---------
# Logging
# --------
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}



# -------------------
# Command Valedation
# -------------------
check_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        log_error "$1 is not installed"
        exit 1
    fi
}


# ----------------
# K8s Valedation
# ----------------
check_cluster() {

    check_command kubectl

    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Cannot connect to Kuberntes cluster"
        exit 1
    fi

    log_success "Connect to Kubernetes cluster"
}


# ------------
# Create Dir
# ------------
prepare_workspace() {

    mkdir -p "$BACKUP_DIR"
    mkdir -p "$REPORT_DIR"

}

test="Script success"
echo -e "${GREEN}[OK]${NC} ${test}"

