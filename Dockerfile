FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install all dependencies for the complete platform
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY shared_lib ./shared_lib
COPY services ./services

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]