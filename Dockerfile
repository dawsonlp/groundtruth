FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project manifest and install dependencies
COPY pyproject.toml README.md /app/
RUN uv sync --no-install-project

# Copy source code and models
COPY src /app/src
COPY models /app/models
RUN uv sync

ENV PYTHONPATH="/app/src"
ENV GROUNDTRUTH_WORKSPACE_ROOT="/workspace/groundtruth"
ENV PORT=9481
ENV PYTHONUNBUFFERED=1

EXPOSE 9481

CMD ["uv", "run", "uvicorn", "groundtruth.service.app:app", "--host", "0.0.0.0", "--port", "9481"]

