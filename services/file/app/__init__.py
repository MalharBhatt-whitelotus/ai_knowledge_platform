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

 * Database Design *

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


* Document Model *
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


* Doc Schema *
1. Upload Request Schema

This defines the metadata the client sends along with the PDF.

Remember: UploadFile itself should not be inside a Pydantic model. FastAPI handles file uploads separately using File(...) and form fields using Form(...).

So your request schema should only contain the non-file metadata.

For example:

class DocumentUploadRequest(BaseModel):
    title: str
    description: str | None = None

Then your route looks like:

@router.post("/upload")
async def upload_document(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
):
    ...

Or you can map those form fields into a schema inside the route if you prefer.

2. Upload Response Schema

This is what the client receives after a successful upload.

It should not expose internal implementation details such as:

storage path
server file name
local filesystem location

Instead, return information that the client actually needs.

For example:

class DocumentUploadResponse(BaseModel):
    id: UUID
    filename: str
    status: DocumentStatus
    message: str

Example response:

{
    "id": "7f73d2aa-8f45-4c89-b9d2-c69b79ef27d3",
    "filename": "python_notes.pdf",
    "status": "UPLOADED",
    "message": "Document uploaded successfully."
}
3. Document Detail Schema

We'll need this in Feature 3.3 – Get Document.

class DocumentResponse(BaseModel):
    id: UUID
    owner_id: UUID
    original_filename: str
    content_type: str
    file_size: int
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

Notice it doesn't include:

extracted text
chunks
embeddings
storage path

Those belong to other services or are internal details.

4. Document List Schema

For Feature 3.2 – List Documents, we'll probably return a collection.

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int

This makes pagination straightforward later.

So what should your schemas define?

For this feature, think in terms of API contracts, not database tables.

Schema	Purpose	Used In
DocumentUploadRequest	Metadata supplied with the upload	POST /documents/upload
DocumentUploadResponse	Confirmation after upload	POST /documents/upload
DocumentResponse	Full document details	GET /documents/{id}
DocumentListResponse	Paginated document listing	GET /documents


For Feature 3.1 (Upload Document)

Your service will eventually do something like:

await storage.save_file(...)
await repository.create_document(...)
await publisher.publish_document_uploaded(...)

Notice that the repository only handles the Document table.

What methods should the repository have?

For the upload feature, you don't need CRUD yet. Only implement what the feature requires.


* Doc Repository *
Required for Feature 3.1
class DocumentRepository:

    async def create(...)

    async def get_by_id(...)

    async def get_by_stored_filename(...)
1. create()

Purpose:

Insert a new document into the database.

Example:

async def create(
    self,
    document: Document,
    db: AsyncSession,
) -> Document:
    ...

This method should:

Add the model
Commit
Refresh
Return the saved document

Nothing else.

2. get_by_id()

Purpose:

Used later for:

GET /documents/{id}

and

DELETE /documents/{id}

Example:

async def get_by_id(
    self,
    document_id: UUID,
    db: AsyncSession,
) -> Document | None:
    ...
3. get_by_stored_filename()

Why?

Because your service will generate a UUID filename.

Imagine:

invoice.pdf

↓

4fda8a34-acde-4d....

Before saving, you can verify uniqueness if needed.

Example:

async def get_by_stored_filename(
    self,
    stored_filename: str,
    db: AsyncSession,
) -> Document | None:
    ...
Future Methods

Don't implement these yet.

We'll add them when the corresponding feature arrives.

list_documents()

update_status()

delete()

count()

search()

filter()

get_by_owner()

exists()

Only build what the current feature needs.

What should the repository NOT do?

❌ Don't do this:

async def upload_pdf(...):
    save_file(...)
    extract_text(...)
    create_embeddings(...)
    ...

That's the service layer's job.

Repository Example
class DocumentRepository:

    async def create(...):
        ...

    async def get_by_id(...):
        ...

    async def get_by_stored_filename(...):
        ...

Very small.

Very focused.

The Service Will Orchestrate Everything

Later your service will look like:

Receive Upload
      │
      ▼
Validate PDF
      │
      ▼
Generate UUID Filename
      │
      ▼
Storage.save_file()
      │
      ▼
Repository.create()
      │
      ▼
RabbitMQ.publish()
      │
      ▼
Return Response

Notice that the service coordinates multiple components.

Should you create a BaseRepository?

Since this is a microservices project with multiple services, yes—but not yet.

Later, in packages/common/database/, we can introduce a generic base repository for common operations like create, get_by_id, delete, and exists. Then each service-specific repository can inherit from it and only implement methods unique to that entity.

For now, keep DocumentRepository explicit. It makes the architecture easier to understand while you're building the platform.

My Recommendation

For Feature 3.1, implement exactly these three methods:

class DocumentRepository:

    async def create(...)

    async def get_by_id(...)

    async def get_by_stored_filename(...)

Don't add update, delete, or list yet. We'll implement those when we reach Features 3.2–3.5. This keeps each feature focused and avoids writing code that isn't used yet.


* Storage Abstraction *
Excellent. This is one of the architectural decisions that separates a production-ready application from a beginner project.

Most tutorials do this:

with open(file_path, "wb") as f:
    f.write(file.read())

directly inside the service.

❌ That tightly couples your service to the local filesystem.

Instead, we're going to use the Strategy Pattern through a storage abstraction.

Step 4 – Storage Abstraction
Goal

The DocumentService should not know where files are stored.

It should only know that it can:

Save a file
Read a file
Delete a file

Whether those files live on:

Local disk
AWS S3
Azure Blob Storage
Google Cloud Storage
MinIO

should be completely hidden.

Architecture
                Document Service
                      │
                      ▼
              Storage Interface
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Local Storage               S3 Storage
        │                           │
        ▼                           ▼
 Local Filesystem             Amazon S3

Notice that DocumentService never changes.

Only the implementation changes.

Folder Structure

I recommend this structure:

app/
├── storage/
│   ├── __init__.py
│   ├── storage_interface.py
│   ├── local_storage.py
│   └── exceptions.py

Later you can add:

storage/
├── s3_storage.py
├── minio_storage.py
├── azure_storage.py

without touching the service layer.

What Should the Interface Define?

The interface should define the operations that every storage provider must implement.

For this project:

class StorageProvider:

    async def save(...)

    async def delete(...)

    async def download(...)

    async def exists(...)

These are the core operations.

1. Save

Purpose:

UploadFile

↓

Store File

↓

Return Storage Path

Suggested signature:

async def save(
    self,
    file: UploadFile,
    filename: str,
) -> str:
    ...

Returns:
uploads/documents/uuid.pdf

2. Delete

Purpose:

Delete Document

↓

Delete File

Signature:

async def delete(
    self,
    path: str,
) -> None:
    ...
3. Download

Purpose:

Later:

GET /documents/{id}/download

Signature:

async def download(
    self,
    path: str,
) -> bytes:
    ...

or return a file stream, depending on how you implement downloads.

4. Exists

Purpose:

Useful before deletion or replacement.

async def exists(
    self,
    path: str,
) -> bool:
    ...
Why Not Add More Methods?

Avoid adding methods like:

move()

rename()

copy()

compress()

encrypt()

until a feature actually requires them.

Follow YAGNI (You Aren't Gonna Need It).

The Service Flow

Later your upload service will look like this:

Receive Upload
      │
      ▼
Validate File
      │
      ▼
Generate UUID Filename
      │
      ▼
storage.save(...)
      │
      ▼
Repository.create(...)
      │
      ▼
RabbitMQ.publish(...)
      │
      ▼
Return Response

Notice the service never opens a file itself.

Dependency Injection

Instead of creating the storage class inside the service:

❌ Don't do this:

storage = LocalStorage()

Inject it:

class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        storage: StorageProvider,
    ):
        self.repository = repository
        self.storage = storage

That makes testing much easier because you can replace the real storage with a fake or mock implementation.

Should We Make It an Abstract Base Class?

Yes.

Use Python's abc module.

Conceptually:

class StorageProvider(ABC):

    @abstractmethod
    async def save(...):
        ...

    @abstractmethod
    async def delete(...):
        ...

    @abstractmethod
    async def download(...):
        ...

    @abstractmethod
    async def exists(...):
        ...

This guarantees that every storage backend implements the required methods.

Future Expansion

Later, adding S3 becomes straightforward:

class S3Storage(StorageProvider):
    async def save(...):
        ...

    async def delete(...):
        ...

    async def download(...):
        ...

    async def exists(...):
        ...

No changes are needed in DocumentService.

Where Are We in Epic 3?
Feature 3.1 – Upload Document

✅ Step 1 - Document Model
✅ Step 2 - Schemas
✅ Step 3 - Repository
🔄 Step 4 - Storage Abstraction
⬜ Step 5 - Local Storage Implementation
⬜ Step 6 - Upload Service
⬜ Step 7 - Upload API
⬜ Step 8 - RabbitMQ Publisher
⬜ Step 9 - Tests
One Improvement I'd Recommend

Instead of naming the interface StorageInterface, I'd call it StorageProvider.

Why?

Because it's not just an interface—it represents a provider capable of storing files. Names like StorageProvider, EmailProvider, and CacheProvider are common in production code and make implementations like LocalStorageProvider or S3StorageProvider read naturally. It also aligns nicely with dependency injection:

def __init__(
    self,
    storage: StorageProvider,
):
    ...

That reads like a capability rather than an implementation detail, and it scales well as you add more storage backends.
"""