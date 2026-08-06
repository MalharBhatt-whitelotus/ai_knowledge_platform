# 🚀 AI Knowledge Platform

> A scalable, AI-powered Knowledge Management Platform built using a Microservices Architecture with FastAPI, PostgreSQL, RabbitMQ, ChromaDB, Docker, JWT Authentication, Sentence Transformers, and Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-success)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-SentenceTransformers-red)
![License](https://img.shields.io/badge/License-MIT-green)

# 📖 Overview

The AI Knowledge Platform is an enterprise-ready backend built around an event-driven microservices architecture. Documents are uploaded, processed asynchronously through RabbitMQ, parsed into text, chunked, embedded using Sentence Transformers, indexed in ChromaDB, and made available for semantic search. The project is designed as the foundation for a production-ready RAG application.

---

# ✨ Features

- API Gateway
- JWT Authentication & Refresh Tokens
- Role-Based Access Control (RBAC)
- File Upload & Metadata Management
- PDF, DOCX, PPTX, XLSX & TXT Parsing
- Background Processing using RabbitMQ
- Worker Service
- Embedding Service (Sentence Transformers)
- Search Service (ChromaDB)
- Semantic Search
- Async FastAPI Microservices
- Dockerized Deployment
- Shared Library
- Structured Logging
- Internal Service-to-Service APIs

---

# 🏗 Architecture

```text
Client
   │
API Gateway
   │
 ├──────────────┬─────────────┬────────────┬───────────────┐
 │              │             │            │               │
Auth        File Service  Search Svc  Embedding Svc   Worker
                                   │
                               RabbitMQ
                                   │
Download → Parse → Chunk → Embeddings → ChromaDB
                                   │
                             Semantic Search
```

---

# 📂 Services

| Service | Responsibility |
|---------|----------------|
| API Gateway | Request routing |
| Auth Service | JWT, Users, RBAC |
| File Service | Upload & metadata |
| Embedding Service | Chunking & embeddings |
| Search Service | ChromaDB semantic retrieval |
| Worker Service | RabbitMQ consumers & background jobs |
| Shared Library | Common utilities |

---

# 🔄 Document Processing Pipeline

```text
Upload Document
      │
      ▼
Store Metadata
      │
      ▼
Publish RabbitMQ Event
      │
      ▼
Worker Downloads File
      │
      ▼
Document Parser
      │
      ▼
Chunk Text
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
Semantic Search
```

---

# 🛠 Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- RabbitMQ
- ChromaDB
- Sentence Transformers
- Docker
- Pydantic v2
- Alembic
- httpx

---

# 🚀 Getting Started

```bash
git clone https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform.git
cd ai_knowledge_platform
docker compose up --build
```

---

# 🔮 Roadmap

- [x] Authentication
- [x] File Service
- [x] Worker Service
- [x] Embedding Service
- [x] Search Service
- [x] RabbitMQ Pipeline
- [x] ChromaDB Integration
- [ ] LLM Answer Generation
- [ ] Conversation Memory
- [ ] Hybrid Search
- [ ] Kubernetes
- [ ] CI/CD
- [ ] Monitoring

---

# 🤝 Contributing

Pull requests are welcome.

---

# 📄 License

MIT License.

---

# 👨‍💻 Author

**Malhar Bhatt**

GitHub: https://github.com/MalharBhatt-whitelotus

---

⭐ If you like this project, consider giving it a star.
