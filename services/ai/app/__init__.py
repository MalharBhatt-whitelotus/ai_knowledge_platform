"""
Epic 4 – Search & Retrieval (RAG)
Feature 4.1 – Semantic Search
⬜ Create Ask Question API

⬜ Validate request

⬜ Generate query embedding

⬜ Search ChromaDB

⬜ Return top-k chunks

Flow:

Question

↓

Embedding Service

↓

Query Vector

↓

ChromaDB

↓

Top K Chunks
Feature 4.2 – Prompt Builder

Build the context for the LLM.

Example:

Question:

"What is FastAPI?"

Context:

Chunk 1...

Chunk 2...

Chunk 3...
Feature 4.3 – AI Service

This is where your AI Service becomes active.

Responsibilities:

Receive Prompt

↓

Call OpenAI

↓

Return Answer

You'll get to practice:

✅ Async AI Requests
✅ httpx
✅ Timeouts
✅ Retry Logic
✅ LLM APIs
Feature 4.4 – RAG Pipeline
User Question

↓

Generate Embedding

↓

Vector Search

↓

Top Chunks

↓

Prompt Builder

↓

OpenAI

↓

Answer

This is the core retrieval-augmented generation workflow.

Feature 4.5 – Streaming Responses

Instead of waiting for the full response:

User

↓

OpenAI Stream

↓

Gateway

↓

Client

You'll learn streaming APIs and improve the user experience.

Epic 5 – Production Features

Once the RAG pipeline works, focus on making it production-ready.

⬜ Retry Policies
⬜ Dead Letter Queue (DLQ)
⬜ RabbitMQ Retry Exchanges
⬜ Redis Cache
⬜ Background Scheduling with Celery
⬜ Rate Limiting
⬜ Observability & Metrics
⬜ Integration Tests
⬜ Load Testing
Overall Progress

I'd estimate your project like this:

Foundation                 ████████████████████ 100%

Authentication             ████████████████████ 100%

Document Upload            ████████████████████ 100%

Background Processing      ████████████████████ 100%

Document Parsing           ████████████████████ 100%

Chunking                   ████████████████████ 100%

Embeddings                 ████████████████████ 100%

Vector Storage             ████████████████████ 100%

Semantic Search            ░░░░░░░░░░░░░░░░░░░   0%

Prompt Engineering         ░░░░░░░░░░░░░░░░░░░   0%

LLM Integration            ░░░░░░░░░░░░░░░░░░░   0%

Streaming                  ░░░░░░░░░░░░░░░░░░░   0%

Redis Cache                ░░░░░░░░░░░░░░░░░░░   0%

Celery                     ░░░░░░░░░░░░░░░░░░░   0%

Production Hardening       ░░░░░░░░░░░░░░░░░░░   0%
My recommendation

The next feature should be Semantic Search.

It naturally builds on everything you've already completed:

User submits a question.
Generate an embedding for the question.
Search ChromaDB for the most relevant chunks.
Build a prompt from those chunks.
Send the prompt to the AI Service.
Return the generated answer.

This is the point where your project transitions from a document processing system into a complete AI-powered knowledge platform.
"""