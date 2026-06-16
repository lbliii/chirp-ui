# Railway deploy image for the chirp-ui live component showcase.
# Build context is the repo root (see /railway.json -> build.dockerfilePath),
# because the app renders from the source templates under src/chirp_ui/templates.
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy the whole repo: the showcase app prefers the in-repo source templates
# (examples/component-showcase/app.py resolves src/chirp_ui/templates relative
# to itself), and `pip install .[showcase]` installs chirp-ui from this tree
# plus kida-templates + bengal-chirp from PyPI.
COPY . .

RUN pip install ".[showcase]"

# Railway injects $PORT at runtime; the entrypoint binds 0.0.0.0:$PORT.
ENV PORT=8080
EXPOSE 8080

CMD ["python", "examples/component-showcase/app.py"]
