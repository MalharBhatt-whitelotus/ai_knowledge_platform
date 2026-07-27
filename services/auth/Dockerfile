FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv pip install --system .

EXPOSE 9000

CMD ["uvicorn", "auth.app.main:app", "--host", "0.0.0.0", "--port", "9000"]