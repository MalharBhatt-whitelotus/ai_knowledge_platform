FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv
RUN uv pip install --system .

COPY . .

EXPOSE 8004

CMD ["uvicorn", "services.search.app.main:app", "--host", "0.0.0.0", "--port", "8004"]