FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    gcc \
    && rm -rf /var/lib/apt/lists/*
    
COPY pyproject.toml .

RUN pip install uv
RUN uv pip install --system .

COPY  . .

EXPOSE 8006

CMD ["uvicorn", "services.worker.app.main:app", "--host", "0.0.0.0", "--port", "8006"]