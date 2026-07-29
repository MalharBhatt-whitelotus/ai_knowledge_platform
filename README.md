# 🚀 AI Knowledge Platform

> A scalable, AI-powered Knowledge Management Platform built using a Microservices Architecture with FastAPI, PostgreSQL, RabbitMQ, Redis, Docker, JWT Authentication, and Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-orange)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

The AI Knowledge Platform is an enterprise-ready backend system designed to ingest, process, index, and query knowledge from documents using modern AI techniques.

The platform follows a **Microservices Architecture**, where every service has its own responsibility and database, making the application highly scalable, maintainable, and production-ready.

---

# ✨ Features

- 🔐 JWT Authentication & Authorization
- 👤 User Management
- 📄 PDF Upload & Storage
- 📚 Document Processing
- 🧠 AI-powered Question Answering
- 🔎 Semantic Search using Embeddings
- 📦 Vector Database Integration
- ⚡ Background Processing with RabbitMQ
- 🚀 Async FastAPI Services
- 🐳 Dockerized Deployment
- 📊 Health Monitoring
- 🔄 REST APIs
- 📁 File Management
- 📈 Scalable Microservices Architecture

---

# 🏗️ Architecture

```
                    +----------------------+
                    |     API Gateway      |
                    +----------+-----------+
                               |
       ---------------------------------------------------------
       |          |           |          |          |           |
       |          |           |          |          |           |
+-------------+ +-----------+ +----------+ +--------------+ +-------------+
| Auth Service| |User Service| |File Service| |Embedding Svc| |Worker Svc |
+-------------+ +-----------+ +----------+ +--------------+ +-------------+
       |              |             |              |               |
       -------------------------------------------------------------
                               |
                         PostgreSQL
                               |
                        RabbitMQ Queue
                               |
                            Redis Cache
                               |
                         Vector Database
                               |
                         AI / LLM Provider
```

---

# 🛠️ Tech Stack

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy (Async)
- Alembic
- Pydantic v2

## Database

- PostgreSQL

## Authentication

- JWT
- OAuth2 Password Flow
- Passlib (Password Hashing)

## Messaging

- RabbitMQ

## Cache

- Redis

## AI Stack

- OpenAI API
- Embeddings
- RAG
- Vector Search

## Infrastructure

- Docker
- Docker Compose

---

# 📂 Project Structure

```
ai_knowledge_platform/

│
├── api_gateway/
│
├── auth_service/
│
├── user_service/
│
├── file_service/
│
├── embedding_service/
│
├── worker_service/
│
├── shared/
│
├── docker/
│
├── docs/
│
├── scripts/
│
├── docker-compose.yml
│
└── README.md
```

---

# ⚙️ Services

## 🔐 Auth Service

Responsible for

- User Login
- User Registration
- JWT Token Generation
- JWT Validation
- Password Hashing

---

## 👤 User Service

Responsible for

- User CRUD
- Profile Management
- Roles
- Permissions

---

## 📄 File Service

Responsible for

- Upload PDFs
- Store Metadata
- Extract Text
- File Management

---

## 🧠 Embedding Service

Responsible for

- Text Chunking
- Embedding Generation
- Vector Storage
- Semantic Search

---

## ⚙️ Worker Service

Responsible for

- Background Tasks
- RabbitMQ Consumers
- Document Processing
- AI Pipelines

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform.git

cd ai_knowledge_platform
```

---

## Create Environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example

```env
DATABASE_URL=
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256

REDIS_URL=

RABBITMQ_URL=

OPENAI_API_KEY=

VECTOR_DB_URL=
```

---

# 🐳 Docker

Build everything

```bash
docker compose up --build
```

Run in background

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

---

# 🗄️ Database Migration

Generate migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migration

```bash
alembic upgrade head
```

---

# 🧪 Running Tests

```bash
pytest
```

With Coverage

```bash
pytest --cov
```

---

# 📌 API Documentation

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔄 AI Pipeline

```
Upload PDF
      │
      ▼
Extract Text
      │
      ▼
Chunk Document
      │
      ▼
Generate Embeddings
      │
      ▼
Store in Vector DB
      │
      ▼
User Query
      │
      ▼
Similarity Search
      │
      ▼
LLM Response
```

---

# 📈 Roadmap

- [x] Authentication
- [x] User Service
- [x] File Upload
- [x] RabbitMQ
- [x] Docker
- [x] Async Architecture
- [x] JWT
- [ ] Embedding Pipeline
- [ ] Vector Database
- [ ] AI Chat
- [ ] RAG Pipeline
- [ ] Kubernetes Deployment
- [ ] CI/CD
- [ ] Monitoring
- [ ] Prometheus & Grafana

---

# 🤝 Contributing

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "feat: add new feature"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Malhar Bhatt**

GitHub:
https://github.com/MalharBhatt-whitelotus

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.
