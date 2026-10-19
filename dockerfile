FROM python:3.12-slim

# get the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1. install dependencies only (cached until pyproject/lock change)
COPY README.md ./
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2. copy the code and install the project itself
COPY src ./src
RUN uv sync --frozen --no-dev

# use the project's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "expensetracker.main:app", "--host", "0.0.0.0", "--port", "8000"]