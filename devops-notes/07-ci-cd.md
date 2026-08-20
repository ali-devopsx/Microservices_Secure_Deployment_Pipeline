# CI/CD

Using GitHub Actions. 3 workflows.

## ci-cd.yml (tests + build)

Triggers on push/PR to main. First it runs tests with a PostgreSQL service container. Then builds the Docker image with Buildx and pushes to Docker Hub as `alidevopsx/cyber-portfolio:latest` plus a SHA tag.

## security-scan.yml

Triggers on push/PR to main and also runs nightly at 2AM. Does two things:
1. Bandit scan on the Python code (`bandit -r app/ --severity-level high`)
2. Trivy scan on the Docker image for vulnerabilities

Trivy is set to `exit-code: "0"` so it doesn't actually fail the build, just reports. There's a `.trivyignore` file with some CVEs to skip.

## deploy.yml

Triggers on push to main. Builds the Docker image and then applies `k8s/django-deployment.yaml` on a self-hosted runner. Note: it only deploys the Django deployment, not all the K8s resources.

## The full flow

Push to main -> tests run -> security scan -> image built and pushed -> deployed to K8s

## Things to fix

Trivy should actually fail the build on critical vulnerabilities. The deploy workflow should apply all K8s resources not just the deployment. And there's no staging environment - changes go straight to production.
