# my dockerfile for the django project
# i learned docker from some tutorials on youtube and this is my own version of it

# =============================================
# PART 1 : build stage (installing everything)
# =============================================

# i use python 3.11 slim because it is smaller than the normal python image
FROM python:3.11-slim AS builder

# this stops python from creating .pyc files on disk
ENV PYTHONDONTWRITEBYTECODE=1

# this makes the logs show up right away (no buffering)
ENV PYTHONUNBUFFERED=1

# dont save the pip cache and dont check pip version everytime
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# this is the folder that we will use inside the container
WORKDIR /app

# update apt and install the tools that we need to compile some python packages
# --no-install-recommends means it will not install extra things we dont need
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# first i copy only the requirements file and nothing else
# because if this file changes docker will only rebuild from here not from the start
COPY app/requirements.txt .

# upgrade pip and the build tools first (they were giving me errors before)
RUN pip install --upgrade pip==25.3 wheel==0.46.2 setuptools

# now install all the packages that are inside requirements.txt
# and also install bandit (security scanner) and gunicorn (the server)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir bandit gunicorn

# copy my whole app so that bandit can scan all the files
COPY app/ .

# run bandit and if it finds a high level problem the build will stop
RUN bandit -r . -x ./venv,./env,./tests --severity-level high || exit 1


# =============================================
# PART 2 : final stage (the actual app image)
# =============================================

# another python image for the final version of the container
FROM python:3.11-slim AS final

# i put the same env vars here again just to be safe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# working directory again
WORKDIR /app

# upgrade pip again in the final image too
RUN pip install --upgrade pip==25.3 wheel==0.46.2 setuptools

# install only the runtime packages here (keeps the image smaller)
# libpq5 is for postgresql and netcat is used to check if the database is up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# make a new user named ali because i dont want to run the app as root
RUN useradd -u 8888 -m ali

# copy everything that we installed in part 1 to this image
COPY --from=builder /usr/local /usr/local

# copy my app code into the container
# --chown=ali:ali means the user ali owns these files
COPY --chown=ali:ali app/ .

# give ali permission to everything in the app folder
RUN chown -R ali:ali /app

# make the staticfiles folder and give it to ali
# (django needs this folder for the css and js files)
RUN mkdir -p /app/staticfiles && chown -R ali:ali /app/staticfiles

# now we switch to the ali user (not root anymore)
USER ali

# healthcheck that checks every 30 seconds if the app is working
HEALTHCHECK --interval=30s --timeout=5s --start-peroid=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# the app uses port 8000
EXPOSE 8000

# copy the entrypoint script and make it runnable
COPY --chown=ali:ali entrypoint.sh .
RUN chmod +x entrypoint.sh

# when the container starts run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
