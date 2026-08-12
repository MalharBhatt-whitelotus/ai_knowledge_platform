<div align="center">

# 🧠 AI Knowledge Platform

**A production-grade, event-driven microservices platform for Retrieval-Augmented Generation (RAG)**

Upload documents → parse & chunk → embed → index → semantically search → generate AI answers.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-4-FF6600?logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![Redis Stack](https://img.shields.io/badge/Redis%20Stack-Cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-6E56CF)](https://www.trychroma.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
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

*Badges are served live by [Badgen](https://badgen.net/) from the GitHub API, so the counts above update automatically as the repository changes.*

</div>

---

## 📖 Overview

**AI Knowledge Platform** is an enterprise-style backend that turns unstructured documents into a searchable, conversational knowledge base. It follows an **event-driven microservices architecture**: every service owns a single responsibility, persists only the data it needs, communicates with its peers over well-defined internal HTTP APIs, and scales independently behind an API Gateway.

When a document is uploaded, it flows asynchronously through the system — parsed, chunked, embedded, vectorized, and made available for **semantic search** and **LLM-powered Q&A** — without blocking the client. A dedicated Worker service consumes upload events off RabbitMQ and drives the pipeline end-to-end, while a separate Celery worker and beat scheduler handle periodic housekeeping tasks. Redis backs both response caching and per-service rate limiting, and Prometheus scrapes metrics from every FastAPI service and the Celery worker for observability.

This project is built as a reference implementation for a production-ready **RAG (Retrieval-Augmented Generation)** system, and doubles as a teaching example of how to structure a multi-service Python backend: consistent layering, a shared library instead of copy-pasted boilerplate, typed Pydantic contracts at every boundary, and infrastructure-as-code via Docker Compose.

### Design principles

- **Single-responsibility services** — Auth only knows about identity, File only knows about storage/metadata, Embedding only knows about turning text into vectors, and so on. No service reaches into another's database.
- **Contracts over convenience** — every inter-service call and every client-facing endpoint is defined by an explicit Pydantic request/response schema, so breaking changes are visible at the type level, not discovered at runtime.
- **Asynchronous by default** — anything that can block (parsing a 50-page PDF, calling an embedding model, calling an LLM) happens off the request/response cycle, driven by RabbitMQ events or read from cache.
- **Fail loudly, recover gracefully** — a message that fails processing is retried with an incrementing `x-retry-count` header and eventually routed to a dead-letter queue instead of being silently dropped or retried forever.
- **Shared, not duplicated** — cross-cutting concerns (config loading, logging, RBAC, rate limiting, retry policies, health checks, metrics, the FastAPI app factory itself) live once in `shared_lib` and are imported by every service.

---

## ✨ Key Features

| Category | Capabilities |
|---|---|
| 🔐 **Auth & Security** | JWT access tokens, `pwdlib`/Argon2 & bcrypt password hashing, Role-Based Access Control (RBAC) via reusable dependencies (e.g. `user_only`) |
| 📂 **File Management** | Multi-format upload (PDF, DOCX, PPTX, XLSX, TXT), metadata tracking, status lifecycle (`in_queue → ready_for_processing → completed / rejected`) |
| ⚙️ **Async Processing** | RabbitMQ-driven event pipeline (`aio-pika`), dedicated Worker consumer, Celery + Celery Beat for scheduled/background tasks, retry & dead-letter-queue publishing |
| 🧩 **Chunking & Embeddings** | Pluggable chunker factory (recursive chunking via LangChain text splitters), Sentence-Transformers embedding generation |
| 🔎 **Semantic Search** | ChromaDB vector indexing and similarity retrieval |
| 🤖 **AI / RAG** | LLM-backed question answering (OpenAI / Google Gen AI) with streaming responses |
| 🚪 **API Gateway** | Single entry point for routing and cross-cutting concerns |
| 🛡 **Resilience** | Redis-backed rate limiting, `tenacity`-based retry policies/decorators, centralized exception handling & middleware |
| 📈 **Observability** | Prometheus metrics (`prometheus-client`) exposed by every service and by the Celery worker, shared `/health` endpoints, structured logging via `structlog` |
| 🐳 **Infrastructure** | Fully Dockerized, shared base image, healthchecks, Alembic migrations, PostgreSQL 17, Redis Stack |
| 🧪 **Testing** | Integration tests (health, file upload, end-to-end RAG flow) and Locust load-test scripts for upload & RAG endpoints |
| 🧰 **DX Tooling** | Jinja2-based code-generator scripts to scaffold new microservices in seconds |

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
        └────────────┘         └─────────────┘               └───────┬──────┘
                                                                       │
                                                        ┌──────────────┼───────────────┐
                                                        │              │               │
                                                 ┌──────▼──────┐┌──────▼──────┐ ┌───────▼───────┐
                                                 │ Redis Stack ││Celery Worker│ │  Celery Beat  │
                                                 │  (Cache)    ││   :9000     │ │ (Scheduler)   │
                                                 └─────────────┘└──────┬──────┘ └───────────────┘
                                                                       │
                                                                ┌──────▼──────┐
                                                                │ Prometheus  │
                                                                │   :9090     │
                                                                └─────────────┘
```

---

## 🔄 Document Processing Pipeline

```text
 1. Client uploads document          →  File Service (RBAC-protected, user only)
 2. Metadata persisted               →  PostgreSQL (status = in_queue)
 3. "file.uploaded" event published  →  RabbitMQ (aio-pika)
 4. Worker consumer picks up event   →  Downloads file bytes from File Service (internal API)
 5. Document parsed to text          →  PDF / DOCX / PPTX / XLSX / TXT parsers
 6. Text split into chunks           →  RecursiveChunker (1000-char chunks, 200-char overlap)
 7. Chunks embedded                  →  Embedding Service (all-MiniLM-L6-v2, normalized vectors)
 8. Vectors indexed                  →  Search Service → ChromaDB (file_id + owner_id as metadata)
 9. File status updated              →  in_queue → ready_for_processing → completed / rejected
10. Failed messages retried / DLQ'd  →  RetryPublisher (x-retry-count header, retry & DLQ exchanges)
11. Client asks a question           →  AI Service retrieves context (Search) + generates/streams an answer
```

### The RAG (question-answering) flow in detail

```text
 1. Client calls POST /ask on the AI Service with {question, top_k}
 2. AI Service asks the Search Service for the top_k most relevant chunks
 3. A deterministic cache key is derived (SHA3-256 of the lower-cased question + retrieved chunk content)
 4. On a cache hit, the cached answer is returned immediately (Redis, TTL-based)
 5. On a cache miss, a grounded prompt is built from a fixed system prompt + numbered context chunks
 6. The prompt is sent to the configured Gen AI model (Google Gemini via google-genai, e.g. gemini-2.5-flash)
 7. The model is instructed to answer ONLY from the supplied context, and to say so plainly if it can't
 8. The answer is cached under the same key and returned to the client
 9. POST /ai/stream follows the same steps but streams tokens back as they're generated
```

This gives the platform **grounded answers** (the LLM only sees retrieved chunks, reducing hallucination), **low-latency repeat queries** (identical question + identical retrieved context = cache hit, no LLM call), and **cheap experimentation** (swap the retrieval `top_k`, the chunk size, or the underlying Gen AI model independently of each other).

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
| **Worker** | `8006` | Consumes RabbitMQ events and drives the async processing pipeline (chunking, retries, DLQ) |
| **Celery Worker** | `9000` | Runs Celery background tasks (e.g. cleanup) with Prometheus metrics |
| **Celery Beat** | — | Schedules periodic Celery tasks |
| **Prometheus** | `9090` | Scrapes `/health` and metrics endpoints from every service |
| **Shared Library** | — | Cross-service config, enums, logging, DB base classes, RBAC dependencies, rate limiting, retry policies, observability |

Every FastAPI service is independently containerized, exposes a `/health` endpoint, and follows the same internal layout: `api/ → services/ → repositories/ → models/ → schemas/`.

### Service deep-dive

<details>
<summary><strong>🔐 Auth Service</strong> — identity, tokens, and RBAC</summary>

- Owns the `user_auth` table in PostgreSQL: `user_id`, `first_name`, `last_name`, `email`, `username`, `password_hash`, `role`, `is_active`, `is_verified`, timestamps.
- Passwords are hashed with `pwdlib` (Argon2) / Passlib + bcrypt — plaintext passwords are never persisted.
- `POST /register_user` creates an account with a default `role=user`; an `admin` role exists for elevated access.
- `POST /login_user` authenticates by username/password and returns a `Bearer` access + refresh token pair.
- `POST /me` and internal current-user resolution back the shared `RoleChecker` dependency (`user_only`, `admin_only`, `user_or_admin` in `shared_lib/dependencies/role_checker.py`), which every other service uses to enforce RBAC on protected routes.
</details>

<details>
<summary><strong>📂 File Service</strong> — upload, storage, and lifecycle tracking</summary>

- Owns the `files` table: `file_id`, `owner_id`, `original_filename`, `stored_filename`, `content_type` (`pdf` / `txt` / `docx` / `xlsx` / `pptx`), `file_size`, `storage_path`, `status`, timestamps.
- `POST /upload_file` is RBAC-protected (`user_only`) and returns immediately with a `file_id` and `in_queue` status — processing happens asynchronously.
- Exposes internal-only endpoints consumed by the Worker service: fetching metadata, streaming raw bytes, extracting plain text, and updating the processing `status`.
- File status follows the lifecycle `in_queue → ready_for_processing → completed / rejected`, giving clients a simple way to poll for readiness.
</details>

<details>
<summary><strong>🧩 Embedding Service</strong> — text → vectors</summary>

- Loads a `sentence-transformers` model (`all-MiniLM-L6-v2`) once at startup and keeps it resident in memory for low-latency inference.
- `POST /internal/generate_embeddings` accepts a batch of text chunks and returns L2-normalized embedding vectors (cosine-similarity ready).
- Rate-limited to **50 requests/minute** per client via the shared Redis-backed `RateLimiter`.
</details>

<details>
<summary><strong>🔎 Search Service</strong> — vector storage and retrieval</summary>

- `POST /internal/store_embedding` persists chunk text + embeddings + `file_id`/`owner_id` metadata into ChromaDB.
- `POST /ask` performs a similarity search and returns the top-`k` matching chunks with their relevance score and metadata — this is the retrieval half of RAG, decoupled from the generation half (which lives in the AI Service).
</details>

<details>
<summary><strong>🤖 AI Service</strong> — RAG orchestration and generation</summary>

- Calls the Search Service to retrieve context, builds a grounded prompt (fixed system prompt instructing the model to answer only from context), and calls the configured Gen AI model (Google Gemini via the `google-genai` SDK).
- Caches answers in Redis keyed by a SHA3-256 hash of the normalized question + retrieved chunk content, so identical questions against identical context skip the LLM call entirely.
- `POST /ask` returns a complete answer; `POST /ai/stream` streams the answer token-by-token as `text/plain`.
- Rate-limited to **30 requests/minute** per client — tighter than other services, reflecting the cost of LLM calls.
</details>

<details>
<summary><strong>⚙️ Worker Service</strong> — the async backbone</summary>

- Consumes `file.uploaded` events from RabbitMQ and drives parsing → chunking → embedding → indexing → status updates.
- Chunking is pluggable via a `ChunkerFactory`; the default `RecursiveChunker` wraps LangChain's `RecursiveCharacterTextSplitter` with a **1000-character chunk size and 200-character overlap**.
- On failure, messages are retried with an incrementing `x-retry-count` header via a dedicated retry exchange, and are ultimately routed to a dead-letter exchange/queue instead of being lost or retried forever.
- Also hosts the **Celery app** (`celery_app.py`) used by the separate `celery_worker` and `celery_beat` containers for scheduled/background jobs such as cleanup.
</details>

<details>
<summary><strong>🚪 Gateway Service</strong> — the single entry point</summary>

- Routes external client traffic to the appropriate downstream service, keeping internal service topology hidden from consumers and giving you one place to add cross-cutting concerns (auth, rate limiting, logging) at the edge.
</details>

---

## 🛠 Tech Stack

<table>
<tr>
<td valign="top">

**Backend**
- FastAPI (async)
- Pydantic v2 (+ `pydantic-settings`)
- SQLAlchemy (async) + Alembic
- Uvicorn

</td>
<td valign="top">

**Data & Messaging**
- PostgreSQL 17 (`asyncpg`, `psycopg`)
- Redis Stack 7 (cache & rate limiting)
- RabbitMQ 4 (via `aio-pika`)
- Celery + Celery Beat
- ChromaDB (vector store)

</td>
<td valign="top">

**AI / ML**
- Sentence-Transformers
- LangChain text splitters
- OpenAI SDK / Google Gen AI SDK (`google-genai`)
- PyMuPDF, `python-docx`, `python-pptx`, `openpyxl`

</td>
<td valign="top">

**Platform & Ops**
- Docker & Docker Compose
- `uv` (dependency management)
- Structlog
- Prometheus (`prometheus-client`)
- `tenacity` (retries)
- JWT / `python-jose` / `pwdlib` / Passlib / Argon2 / bcrypt
- `pytest`, `pytest-asyncio`, Locust (load testing)

</td>
</tr>
</table>

---

## 📦 Repository Structure

```text
ai_knowledge_platform/
├── services/
│   ├── gateway/            # API Gateway
│   ├── auth/                # Authentication & RBAC
│   ├── file/                 # Upload, storage & parsing
│   ├── embedding/       # Embedding generation
│   ├── search/              # Vector search (ChromaDB)
│   ├── ai/                    # RAG orchestration & LLM calls
│   └── worker/            # RabbitMQ consumers, chunking, Celery tasks & beat schedule
├── shared_lib/
│   ├── cache/               # Redis client
│   ├── clients/             # Inter-service HTTP clients (auth, file, embedding, search)
│   ├── config/              # Shared settings
│   ├── constants/          # App-wide constants
│   ├── core/                 # Factory, middleware, exception handler, rate limiter
│   ├── dependencies/    # RBAC role checkers
│   ├── exceptions/       # Custom exception types
│   ├── logger/              # Structlog setup
│   ├── observability/    # Health & Prometheus metrics routes
│   ├── retry/                # Tenacity retry decorators & policies
│   ├── schemas/           # Shared Pydantic schemas (current user, health, error)
│   └── enums.py             # Role, DocType, DocStatus enums
├── scripts/                    # CLI + generator to scaffold new services
├── prometheus/               # Prometheus scrape configuration
├── tests/
│   ├── integration/          # Health, file upload, end-to-end RAG flow tests
│   └── load/                   # Locust load-test scripts (upload & RAG)
├── docker-compose.yml
├── Dockerfile.base           # Shared base image for all services
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

The **Worker** service additionally includes `chunking/` (chunker factory + recursive chunker), `consumers/` & `handlers/` (RabbitMQ event handling), `messaging/` (topology, publisher, retry/DLQ publisher), `tasks/` (Celery tasks such as cleanup), and `celery_app.py`.

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

#### Full settings reference

The shared `Settings` class (`shared_lib/config/settings.py`) is loaded by every FastAPI service and defines the complete set of configurable values. Populate whichever of these apply to the service(s) you're running:

| Variable | Purpose |
|---|---|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT` | PostgreSQL connection |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD` | Redis connection (cache & rate limiter) |
| `REDIS_CACHE_TTL` | TTL (seconds) for cached AI answers |
| `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASSWORD` | RabbitMQ connection |
| `AUTH_URL`, `FILE_URL`, `EMBEDDING_URL`, `SEARCH_URL` | Base URLs the shared inter-service HTTP clients call |
| `OPEN_AI_KEY` | OpenAI API key (optional provider) |
| `GENAI_API_KEY`, `GENAI_MODEL` | Google Gen AI credentials and model name (e.g. `gemini-2.5-flash`) — required by the AI Service |
| `RETRY_ATTEMPTS`, `RETRY_MIN_WAIT`, `RETRY_MAX_WAIT` | Defaults for `tenacity`-based retry policies |
| `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | Broker (RabbitMQ) and result backend (Redis) for Celery |
| `APP_NAME`, `APP_VERSION` | Service metadata surfaced on `/health` |

> The AI Service currently calls **Google Gemini** via the `google-genai` SDK — set `GENAI_API_KEY` and `GENAI_MODEL` in `services/ai/.env` before starting it. The `OPEN_AI_KEY` setting is present for OpenAI-based extensions to the platform.

### 3. Build & run with Docker Compose

```bash
docker compose up --build
```

This will spin up:

- **Infrastructure** — PostgreSQL 17, Redis Stack, RabbitMQ (management UI included), all with healthchecks
- **Shared `ai-base` image** — built once, reused by every service
- **Seven FastAPI microservices** — each on its own port
- **Celery Worker & Celery Beat** — background task execution and scheduling
- **Prometheus** — scraping metrics from every service

### 4. Verify the platform is running

```bash
curl http://localhost:8000/health   # Gateway
curl http://localhost:8001/health   # Auth
curl http://localhost:8002/health   # File
```

| UI | URL |
|---|---|
| RabbitMQ Management | [http://localhost:15673](http://localhost:15673) |
| Redis Stack (RedisInsight) | [http://localhost:8007](http://localhost:8007) |
| Prometheus | [http://localhost:9090](http://localhost:9090) |

---

## 📡 Core API Endpoints

| Method | Endpoint | Service | Description |
|---|---|---|---|
| `POST` | `/register_user` | Auth | Register a new user |
| `POST` | `/login_user` | Auth | Authenticate and issue a JWT access/refresh token pair |
| `POST` | `/logout_user` | Auth | Invalidate the current session |
| `POST` | `/me` | Auth | Get the authenticated user's profile |
| `POST` | `/upload_file` | File | Upload a document for processing *(user only)* |
| `GET`  | `/get_file/{file_id}` | File | Fetch file metadata for the current user |
| `GET`  | `/internal/get_file/{file_id}` | File | Fetch file metadata *(internal)* |
| `GET`  | `/internal/download_file/{file_id}` | File | Stream raw file bytes *(internal)* |
| `GET`  | `/internal/extract_text/{file_id}` | File | Extract plain text from a stored file *(internal)* |
| `POST` | `/internal/status_update/{file_id}` | File | Update a file's processing status *(internal)* |
| `POST` | `/internal/generate_embeddings` | Embedding | Generate embeddings for text chunks *(internal)* |
| `POST` | `/internal/store_embedding` | Search | Persist embeddings to ChromaDB *(internal)* |
| `POST` | `/ask` | Search | Semantic search — returns the top-k relevant chunks |
| `POST` | `/ask` | AI | Get a full, LLM-generated answer (RAG) |
| `POST` | `/ai/stream` | AI | Stream an LLM-generated answer as `text/plain` |

> Endpoints prefixed with `/internal/*` are service-to-service only and are not intended to be called directly by clients. Every service also exposes a `GET /health` endpoint used by Docker healthchecks and Prometheus.

### Example: upload a file

```bash
curl -X POST http://localhost:8000/upload_file \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@/path/to/document.pdf"
```

```json
{
  "file_id": "f_8f1c...",
  "filename": "document.pdf",
  "status": "in_queue",
  "message": "File accepted and queued for processing."
}
```

### Example: ask a question (RAG)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the onboarding policy say about remote work?", "top_k": 5}'
```

```json
{
  "question": "What does the onboarding policy say about remote work?",
  "answer": "According to the uploaded documents, ..."
}
```

`top_k` accepts values between `1` and `19` (Search Service caps at `20`) and defaults to `5`. Identical questions against unchanged source documents are served from the Redis answer cache rather than re-invoking the LLM.

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

### Running tests

Integration tests cover service health, file upload, and the end-to-end RAG flow:

```bash
pytest tests/integration
```

Load tests (Locust) are available for the upload and RAG endpoints:

```bash
locust -f tests/load/locustfile_upload.py
locust -f tests/load/locustfile_rag.py
```

### Metrics & observability

Every FastAPI service and the Celery worker expose Prometheus-compatible metrics (e.g. `http_requests_total`, `http_request_duration_seconds`, Celery task counters/durations), scraped per `prometheus/prometheus.yml`.

### Rate limits (per client, sliding window in Redis)

| Service | Limit |
|---|---|
| Embedding | 50 requests / 60s |
| AI | 30 requests / 60s |

Additional services can opt into the same `RateLimiter` by instantiating it against `RedisClient` and wiring it into `create_app(..., rate_limiter=...)` — see `shared_lib/core/rate_limiter.py` and `shared_lib/core/factory.py`.

---

## 🩺 Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `docker compose up` fails on `ai-base` | The shared base image must build successfully before any service starts (`service_completed_successfully` dependency) — check `Dockerfile.base` for missing system packages. |
| A service's healthcheck never turns green | Confirm its `.env` file has every variable required by `shared_lib/config/settings.py` — a missing required field will crash the app at import time. |
| Uploaded files stay stuck in `in_queue` | Check the Worker service logs and the RabbitMQ Management UI (`:15673`) for messages piling up in the retry or dead-letter queue — this usually means parsing or embedding is failing. |
| `/ask` on the AI Service returns 404 "Search Results not found" | No chunks have been indexed yet for that query, or the corresponding file hasn't finished processing — confirm the file's `status` is `completed`. |
| AI Service fails to start / GenAI errors | Ensure `GENAI_API_KEY` and `GENAI_MODEL` are set in `services/ai/.env`; the Google Gen AI SDK requires both. |
| Answers seem "stale" after re-uploading a document | Answers are cached by a hash of the question + retrieved chunk content — a genuinely new set of retrieved chunks will naturally produce a cache miss and a fresh answer. |

---

## 🔮 Roadmap

- [x] Authentication & RBAC
- [x] File upload & parsing (PDF, DOCX, PPTX, XLSX, TXT)
- [x] RabbitMQ event-driven pipeline with retry/DLQ handling
- [x] Embedding generation
- [x] ChromaDB semantic search
- [x] RAG-based AI answers (with streaming)
- [x] Celery + Celery Beat for background/scheduled tasks
- [x] Prometheus metrics & observability
- [x] Redis-backed rate limiting
- [x] Integration & load test suites
- [ ] Conversation memory / multi-turn chat
- [ ] Hybrid search (keyword + vector)
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline
- [ ] Grafana dashboards on top of Prometheus metrics

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