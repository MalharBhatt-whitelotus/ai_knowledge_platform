FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "services.gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]