FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8005

CMD ["uvicorn", "services.ai.app.main:app", "--host", "0.0.0.0", "--port", "8005"]