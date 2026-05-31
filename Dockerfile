# ===================================
# STAGE 1: Builder
# ===================================

# Use official lightweight Python image to build dependencies
FROM python:3.11-slim AS builder


# Prevent Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1


# Prevent Python from buffering stdout and stderr (helps in logging)
ENV PYTHONUNBUFFERED=1


# Set the working directory inside the container for stage 1
WORKDIR /app


# Install system dependencies needed to compile some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy only the requirements file first to utilize Docker caching
COPY app/requirements.txt .


# Build Python packages and install bandit (Security Tool) + Gunicorn
RUN pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir --user bandit gunicorn


# Copy all source code to stage 1 so bandit can check it
COPY app/ .


# RUN SECURITY SCAN: Bandit will scan the code. If it finds severe bugs, build fails with exit code 1
RUN /root/.local/bin/bandit -r . -x ./venv,./env,./tests --severity-level high || exit 1



# =====================================
# STAGE 2: Final Runtime
# =====================================


# Use the same slim Python image for the clean final container
FROM python:3.11-slim AS final


# Re-defined environment variables for safety
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# Set the official working directory for the application
WORKDIR /app


# Install only minimal runtime libraries needed for PostgreSQL database
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Create a home directory for user ali first to store the secure packages
RUN useradd -u 8888 -m ali


# Copy Python packages from the builder stage to the final stage
COPY --from=builder --chown=ali:ali /root/.local /home/ali/.local


# Copy the globally installed python packages from builder to final stag

# Make sure the copied python packages are accessible in the system path
ENV PATH=/home/ali/.local/bin:$PATH


# Install Gunicorn server safely for production execution
# (Gunicorn is already installed in Stage 1 and copied successfully)


# SECURITY HARDENING: Remove pip entirely from the final runtime image
#RUN pip uninstall -y pip


# SECURITY HARDENING: Safely remove pip and setuptools binaries from the final image
# (Completely secured: Final runtime stage contains no pip binary at all!)


# Copy all your clean Django source code into the container
COPY --chown=ali:ali app/ .


# Security (OSCP): Create a restricted system user to run the app
RUN chown -R ali:ali /app


# FIX PERMISSIONS: Create staticfiles directory and give ownership to ali before switching users
RUN mkdir -p /app/staticfiles && chown -R ali:ali /app/staticfiles


# Switch from root user to the newly created secure user
USER ali



# Inform Docker that the container listens on port 8000 at runtime
EXPOSE 8000


# Copy the entrypoint script and make sure it has execution privileges
COPY --chown=ali:ali entrypoint.sh .
RUN chmod +x entrypoint.sh


# Execute the entrypoint script when the container boots up
ENTRYPOINT ["./entrypoint.sh"]
