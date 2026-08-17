FROM ai-base:latest

WORKDIR /app

COPY services/ai /app/services/ai

EXPOSE 8005

CMD ["uvicorn", "services.ai.app.main:app", "--host", "0.0.0.0", "--port", "8005"]