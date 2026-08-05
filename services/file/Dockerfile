FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8002

CMD ["uvicorn", "services.file.app.main:app", "--host", "0.0.0.0", "--port", "8002"]