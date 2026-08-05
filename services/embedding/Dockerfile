FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8003

CMD ["uvicorn", "services.embedding.app.main:app", "--host", "0.0.0.0", "--port", "8003"]