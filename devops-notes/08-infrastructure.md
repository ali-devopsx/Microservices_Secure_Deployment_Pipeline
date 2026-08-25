# Infrastructure

## What I'm using

No Terraform, no Ansible, no cloud providers. Everything is local.

Docker Compose for local dev. Minikube for Kubernetes. That's pretty much it.

## Helm

There's a `get_helm.sh` script in the root but I'm not actually using Helm anywhere. No charts exist. It's just there in case I need it later.

## Velero + MinIO

MinIO runs inside K8s in the `velero` namespace as local S3-compatible storage. Velero takes daily backups of the cluster.

## What's missing

For a real project I'd need actual cloud infrastructure with IaC. But this is a learning project so local is fine for now.
