FROM ai-base:latest

WORKDIR /app

COPY services/worker /app/services/worker

EXPOSE 8006

CMD ["uvicorn", "services.worker.app.main:app", "--host", "0.0.0.0", "--port", "8006"]