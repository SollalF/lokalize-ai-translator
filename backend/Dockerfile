FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml /app/
COPY ./app /app/app
COPY ./main.py /app/

# Create logs directory
RUN mkdir -p /app/logs

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

EXPOSE 8000

CMD ["python", "main.py"] 