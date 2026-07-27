FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv
RUN uv pip install --system .

COPY . .

EXPOSE 8002

CMD ["uvicorn", "services.file.app.main:app", "--host", "0.0.0.0", "--port", "8002"]