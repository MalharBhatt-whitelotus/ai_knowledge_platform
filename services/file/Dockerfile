FROM ai-base:latest

WORKDIR /app

COPY services/file /app/services/file

EXPOSE 8002

CMD ["uvicorn", "services.file.app.main:app", "--host", "0.0.0.0", "--port", "8002"]