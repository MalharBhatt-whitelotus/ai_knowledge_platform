"""
Epic 3 Features

We'll build this epic feature by feature.

Feature 3.1 – Upload Document
Upload PDF
Validate file
Store metadata
Save file
Publish processing event

Feature 3.2 – List Documents
GET /documents

Pagination, filtering, search.


Feature 3.3 – Get Document
GET /documents/{id}

Feature 3.4 – Download Document
GET /documents/{id}/download

Feature 3.5 – Delete Document

Deletes:

Metadata
File
Vectors (later)

Feature 3.6 – Processing Status
{
    "status": "PROCESSING"
}

Later:

UPLOADED

PROCESSING

EMBEDDED

FAILED

Database Design

We'll start with this model.

documents
──────────────────────────────────────

id (UUID)

owner_id (UUID)

original_filename

stored_filename

content_type

file_size

storage_path

status

created_at

updated_at

Notice we don't store extracted text here.

Why?

Because the Document Service shouldn't know about text extraction.

That belongs to the Processing Service.

Document Lifecycle
UPLOAD
   │
   ▼
UPLOADED
   │
   ▼
PROCESSING
   │
   ▼
EMBEDDED
   │
   ▼
READY

If something fails:

PROCESSING
      │
      ▼
FAILED
Folder Structure

We'll use the same structure as the Auth Service.

services/
└── document/
    ├── app/
    │
    ├── api/
    │   ├── routes/
    │   │   └── document.py
    │   └── router.py
    │
    ├── config/
    ├── database/
    ├── dependencies/
    ├── models/
    │   └── document.py
    │
    ├── repositories/
    │   └── document_repository.py
    │
    ├── schemas/
    │   ├── document_request.py
    │   └── document_response.py
    │
    ├── services/
    │   └── document_service.py
    │
    ├── storage/
    │   ├── local_storage.py
    │   └── storage_interface.py
    │
    ├── messaging/
    │   └── publisher.py
    │
    ├── utils/
    └── main.py
    │
    ├── tests/
    ├── Dockerfile
    └── .env
    
Why a storage/ Package?

Don't save files directly inside the service layer.

We'll define an abstraction:

class StorageProvider:
    async def save(...)
    async def delete(...)
    async def download(...)

Today:

Local Storage

Tomorrow:

Amazon S3

or

MinIO

The service code won't change.

Development Plan

We'll build Feature 3.1 in this order:

Step	Task
1	Document model
2	Document schemas
3	Repository
4	Storage abstraction
5	Local storage implementation
6	Upload service
7	Upload API
8	RabbitMQ publisher (stub initially)
9	Tests

Each step ends with working code.

📌 Our First Task

We'll start with Feature 3.1 – Step 1: Document Model.

We'll create:

DocumentStatus enum
Document SQLAlchemy model
Alembic migration
Repository base integration

This gives us the persistence layer before we build the upload logic.

One architectural improvement before we start

In your previous project, the file itself and its extracted text lived in the same service. For this platform, I'd like to separate responsibilities completely:

Document Service owns the file and its metadata.
Processing Service owns extracted text.
Embedding Service owns embeddings.
Search Service owns vector storage.

That separation will make the platform easier to scale, easier to test, and much easier to extend to new document types in the future.
"""