FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8006

CMD ["uvicorn", "services.worker.app.main:app", "--host", "0.0.0.0", "--port", "8006"]