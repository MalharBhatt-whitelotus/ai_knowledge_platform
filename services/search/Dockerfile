FROM ai-base

WORKDIR /app

COPY . .

EXPOSE 8004

CMD ["uvicorn", "services.search.app.main:app", "--host", "0.0.0.0", "--port", "8004"]