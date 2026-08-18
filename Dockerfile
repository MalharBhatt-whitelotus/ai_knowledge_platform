FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        supervisor \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Python dependency files
COPY pyproject.toml .
COPY uv.lock .

RUN pip install --no-cache-dir uv && \
    uv sync --frozen

# Application
COPY shared_lib ./shared_lib
COPY services ./services

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONPATH=/app

# Application ports
EXPOSE 8000 8001 8002 8003 8004 8005 8006

CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]