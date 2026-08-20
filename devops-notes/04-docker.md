# Docker

## Dockerfile (main app)

I'm using a multi-stage build. First stage (`builder`) installs build tools and pip packages, and runs a Bandit security scan. Second stage copies just the packages into a clean slim image, creates a non-root user called `ali` (UID 8888), and runs Gunicorn.

The healthcheck hits `http://localhost:8000/health/`.

Build with: `docker build -t cyber-portfolio .`

The multi-stage thing is nice because the final image doesn't have gcc and all the build stuff in it. Smaller and more secure.

## Dockerfile.celery

Single stage, same base image. Installs requirements plus `libpq5` for PostgreSQL support. Purges `perl-base` to save some space. Runs `celery -A cyber_portfolio worker --loglevel=info`.

Build with: `docker build -f Dockerfile.celery -t cyber-celery .`

## entrypoint.sh

This is what runs when the container starts. It waits for PostgreSQL to be ready using `nc` (netcat), then runs migrations, collectstatic, and finally starts Gunicorn on port 8000.

## Stuff I noticed

The healthcheck uses `curl` but I don't think curl is actually installed in the final image. Same with `nc` in the entrypoint. These might be issues. Also the Bandit scan only checks for HIGH severity which means medium stuff slips through.
