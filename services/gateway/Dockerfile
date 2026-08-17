FROM ai-base:latest

WORKDIR /app

COPY services/gateway /app/services/gateway

EXPOSE 8000

CMD ["uvicorn", "services.gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]