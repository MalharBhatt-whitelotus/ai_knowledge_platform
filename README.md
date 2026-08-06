<div align="center">

# 🧠 AI Knowledge Platform

**A production-grade, event-driven microservices platform for Retrieval-Augmented Generation (RAG)**

Upload documents → parse & chunk → embed → index → semantically search → generate AI answers.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-FF6600?logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-6E56CF)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)

</div>

---

## 📊 Project Stats

<div align="center">

[![Commits](https://badgen.net/github/commits/MalharBhatt-whitelotus/ai_knowledge_platform/main)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/commits/main)
[![Open PRs](https://badgen.net/github/open-prs/MalharBhatt-whitelotus/ai_knowledge_platform)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/pulls)
[![Merged PRs](https://badgen.net/github/merged-prs/MalharBhatt-whitelotus/ai_knowledge_platform)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/pulls?q=is%3Apr+is%3Amerged)
[![Closed PRs](https://badgen.net/github/closed-prs/MalharBhatt-whitelotus/ai_knowledge_platform)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/pulls?q=is%3Apr+is%3Aclosed)
[![Last Commit](https://badgen.net/github/last-commit/MalharBhatt-whitelotus/ai_knowledge_platform/main)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/commits/main)
[![Contributors](https://badgen.net/github/contributors/MalharBhatt-whitelotus/ai_knowledge_platform)](https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform/graphs/contributors)

*Badges are served live by [Badgen](https://badgen.net/) from the GitHub API, so the counts above update automatically as the repository changes — no manual editing needed.*

</div>

---

## 📖 Overview

**AI Knowledge Platform** is an enterprise-style backend that turns unstructured documents into a searchable, conversational knowledge base. It follows an **event-driven microservices architecture**: every service owns a single responsibility, communicates over well-defined internal APIs, and scales independently behind an API Gateway.

When a document is uploaded, it flows asynchronously through the system — parsed, chunked, embedded, vectorized, and made available for **semantic search** and **LLM-powered Q&A** — without blocking the client.

This project is built as a reference implementation for a production-ready **RAG (Retrieval-Augmented Generation)** system.

---

## ✨ Key Features

| Category | Capabilities |
|---|---|
| 🔐 **Auth & Security** | JWT access/refresh tokens, password hashing (Argon2/bcrypt), Role-Based Access Control (RBAC) |
| 📂 **File Management** | Multi-format upload (PDF, DOCX, PPTX, XLSX, TXT), metadata tracking, pluggable storage providers |
| ⚙️ **Async Processing** | RabbitMQ-driven event pipeline, dedicated Worker service, non-blocking uploads |
| 🧩 **Chunking & Embeddings** | Recursive text chunking, Sentence-Transformers embedding generation |
| 🔎 **Semantic Search** | ChromaDB vector indexing and similarity retrieval |
| 🤖 **AI / RAG** | LLM-backed question answering with streaming responses |
| 🚪 **API Gateway** | Single entry point for routing and cross-cutting concerns |
| 🐳 **Infrastructure** | Fully Dockerized, shared base image, healthchecks, Alembic migrations |
| 🧰 **DX Tooling** | Code-generator scripts to scaffold new microservices in seconds |

---

## 🏗 Architecture

```text
                                   ┌────────────┐
                                   │   Client   │
                                   └─────┬──────┘
                                         │
                                   ┌─────▼──────┐
                                   │ API Gateway│  :8000
                                   └─────┬──────┘
        ┌───────────┬───────────┬───────┼──────────┬────────────┐
        │           │           │       │           │            │
   ┌────▼────┐ ┌────▼────┐ ┌────▼───┐ ┌─▼──────┐ ┌──▼───────┐ ┌──▼──────┐
   │  Auth   │ │  File   │ │Embedding│ │ Search │ │   AI     │ │ Worker  │
   │ :8001   │ │ :8002   │ │ :8003   │ │ :8004  │ │ :8005    │ │ :8006   │
   └────┬────┘ └────┬────┘ └────┬───┘ └───┬────┘ └────┬─────┘ └────┬────┘
        │           │           │         │           │            │
        └─────┬─────┴───────────┴────┬────┴───────────┘            │
              │                      │                              │
        ┌─────▼─────┐         ┌──────▼──────┐               ┌───────▼──────┐
        │ PostgreSQL │         │  ChromaDB   │               │   RabbitMQ   │
        │  (17)      │         │ (Vector DB) │               │(Event Broker)│
        └────────────┘         └─────────────┘               └──────────────┘
                                                                       │
                                                                ┌──────▼──────┐
                                                                │    Redis    │
                                                                │   (Cache)   │
                                                                └─────────────┘
```

---

## 🔄 Document Processing Pipeline

```text
 1. Client uploads document      →  File Service
 2. Metadata persisted           →  PostgreSQL
 3. "file.uploaded" event fired  →  RabbitMQ
 4. Worker consumes event        →  Downloads file from File Service
 5. Document parsed to text      →  PDF / DOCX / PPTX / XLSX / TXT parsers
 6. Text split into chunks       →  Recursive chunker
 7. Chunks embedded              →  Embedding Service (Sentence-Transformers)
 8. Vectors indexed              →  Search Service → ChromaDB
 9. File status updated          →  in_queue → pending → completed
10. Client asks a question       →  AI Service retrieves context + generates answer
```

---

## 📂 Service Directory

| Service | Port | Responsibility |
|---|---|---|
| **Gateway** | `8000` | Single entry point; request routing to downstream services |
| **Auth** | `8001` | Registration, login/logout, JWT issuance, current-user resolution, RBAC |
| **File** | `8002` | Upload, storage, metadata, text extraction, status tracking |
| **Embedding** | `8003` | Generates vector embeddings for text chunks |
| **Search** | `8004` | Stores/queries embeddings in ChromaDB, semantic retrieval |
| **AI** | `8005` | Orchestrates RAG — builds prompts, calls the LLM, streams answers |
| **Worker** | `8006` | Consumes RabbitMQ events and drives the async processing pipeline |
| **Shared Library** | — | Cross-service config, enums, logging, DB base classes, RBAC dependencies |

Every service is independently containerized, exposes a `/health` endpoint, and follows the same internal layout: `api/ → services/ → repositories/ → models/ → schemas/`.

---

## 🛠 Tech Stack

<table>
<tr>
<td valign="top">

**Backend**
- FastAPI (async)
- Pydantic v2
- SQLAlchemy (async) + Alembic
- Uvicorn

</td>
<td valign="top">

**Data & Messaging**
- PostgreSQL 17
- Redis 7
- RabbitMQ 4 (via `aio-pika`)
- ChromaDB

</td>
<td valign="top">

**AI / ML**
- Sentence-Transformers
- LangChain text splitters
- OpenAI / Google Gen AI SDKs

</td>
<td valign="top">

**Platform**
- Docker & Docker Compose
- `uv` (dependency management)
- Structlog
- JWT / `python-jose` / Passlib / Argon2

</td>
</tr>
</table>

---

## 📦 Repository Structure

```text
ai_knowledge_platform/
├── services/
│   ├── gateway/          # API Gateway
│   ├── auth/              # Authentication & RBAC
│   ├── file/               # Upload, storage & parsing
│   ├── embedding/     # Embedding generation
│   ├── search/            # Vector search (ChromaDB)
│   ├── ai/                  # RAG orchestration & LLM calls
│   └── worker/          # RabbitMQ consumers & background jobs
├── shared_lib/          # Shared config, enums, logging, DB, RBAC
├── scripts/               # CLI + generator to scaffold new services
├── docker-compose.yml
├── Dockerfile.base     # Shared base image for all services
├── pyproject.toml
└── README.md
```

Each service under `services/<name>/app/` follows a clean, layered structure:

```text
app/
├── api/routes/        # HTTP route handlers
├── services/           # Business logic
├── repositories/     # Data access layer
├── models/             # ORM models
├── schemas/            # Pydantic request/response models
├── clients/             # Inter-service HTTP clients
├── config/              # Service-specific settings
└── main.py               # FastAPI app factory & startup
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- Python **3.12+** (for local, non-Docker development)
- [`uv`](https://docs.astral.sh/uv/) (recommended for dependency management)

### 1. Clone the repository

```bash
git clone https://github.com/MalharBhatt-whitelotus/ai_knowledge_platform.git
cd ai_knowledge_platform
```

### 2. Configure environment variables

Create a root `.env` file (used by `postgres`, `rabbitmq`, and most services), plus service-level `.env` files where required (`services/auth/.env`, `services/file/.env`, `services/worker/.env`):

```env
# Postgres
POSTGRES_DB=ai_knowledge_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# RabbitMQ
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASSWORD=guest
RABBITMQ_PORT=5672

# App
APP_VERSION=0.1.0
```

> 💡 Use `scripts/templates/service/.env.j2` as a starting point when scaffolding a new service's environment file.

### 3. Build & run with Docker Compose

```bash
docker compose up --build
```

This will spin up:

- Infrastructure → PostgreSQL, Redis, RabbitMQ (with healthchecks)
- Shared `ai-base` image (built once, reused by every service)
- All seven microservices, each on its own port

### 4. Verify the platform is running

```bash
curl http://localhost:8000/health   # Gateway
curl http://localhost:8001/health   # Auth
curl http://localhost:8002/health   # File
```

RabbitMQ Management UI → [http://localhost:15673](http://localhost:15673)

---

## 📡 Core API Endpoints

| Method | Endpoint | Service | Description |
|---|---|---|---|
| `POST` | `/register_user` | Auth | Register a new user |
| `POST` | `/login_user` | Auth | Authenticate and issue JWT tokens |
| `POST` | `/logout_user` | Auth | Invalidate the current session |
| `POST` | `/me` | Auth | Get the authenticated user's profile |
| `POST` | `/upload_file` | File | Upload a document for processing |
| `GET`  | `/get_file/{file_id}` | File | Fetch file metadata |
| `POST` | `/internal/generate_embeddings` | Embedding | Generate embeddings for text chunks *(internal)* |
| `POST` | `/internal/store_embedding` | Search | Persist embeddings to ChromaDB *(internal)* |
| `POST` | `/ask` | Search | Ask a question against indexed documents |
| `POST` | `/ask` | AI | Get an LLM-generated answer (RAG) |
| `POST` | `/ai/stream` | AI | Stream an LLM-generated answer |

> Endpoints prefixed with `/internal/*` are service-to-service only and are not intended to be called directly by clients.

---

## 🧪 Development

### Scaffolding a new microservice

The project ships with generator scripts to create a new, fully-structured service in one command:

```bash
python scripts/cli.py create-service <service_name>
```

This uses `scripts/generator.py` and `scripts/renderer.py` with Jinja2 templates under `scripts/templates/` to produce a consistent `api/ → services/ → repositories/ → models/` layout, `Dockerfile`, and `.env`.

### Running database migrations

Each service that owns a database (Auth, File) manages its own Alembic history:

```bash
cd services/auth
alembic upgrade head
```

### Installing dependencies locally

```bash
uv sync
```

---

## 🔮 Roadmap

- [x] Authentication & RBAC
- [x] File upload & parsing (PDF, DOCX, PPTX, XLSX, TXT)
- [x] RabbitMQ event-driven pipeline
- [x] Embedding generation
- [x] ChromaDB semantic search
- [x] RAG-based AI answers (with streaming)
- [ ] Conversation memory / multi-turn chat
- [ ] Hybrid search (keyword + vector)
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline
- [ ] Observability & monitoring (Prometheus/Grafana)

---

## 🤝 Contributing

Contributions are welcome! To propose a change:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes with clear messages
4. Open a pull request describing the change and motivation

Please keep new services aligned with the existing layered structure (`api → services → repositories → models → schemas`).

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Malhar Bhatt**
GitHub: [@MalharBhatt-whitelotus](https://github.com/MalharBhatt-whitelotus)



---

<div align="center">

⭐ **If you find this project useful, consider giving it a star!**

</div>