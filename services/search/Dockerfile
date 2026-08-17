# syntax=docker/dockerfile:1.7

FROM ai-base:latest

WORKDIR /app

RUN pip install --no-cache-dir "chromadb>=1.0.0"

COPY services/search /app/services/search

EXPOSE 8004

CMD ["uvicorn","services.search.app.main:app", "--host","0.0.0.0","--port","8004"]