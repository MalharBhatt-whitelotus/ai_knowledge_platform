FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8001

CMD ["uvicorn", "services.auth.app.main:app", "--host", "0.0.0.0", "--port", "8001"]