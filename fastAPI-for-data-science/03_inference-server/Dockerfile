FROM python:3.11-slim-bullseye

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy only the dependency files first (for better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (creates .venv)
RUN uv sync --frozen --no-cache

# Copy the application and the pre-trained model
COPY app/ /app/app/
COPY models/ /app/models/

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]
