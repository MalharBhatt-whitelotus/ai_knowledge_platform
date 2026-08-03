"""
Phase 2 – DocumentUploadedConsumer
Responsibility
RabbitMQ Queue
      │
      ▼
Receive Message
      │
      ▼
Deserialize JSON
      │
      ▼
Validate Event
      │
      ▼
Call Handler
      │
      ▼
ACK or NACK

Notice what's not here:

❌ PDF extraction
❌ Chunking
❌ Embedding generation
❌ Database updates
❌ HTTP calls

Those belong to the handler.

Folder
services/
└── worker/
    └── app/
        └── consumers/
            └── document_uploaded_consumer.py
Consumer Responsibilities

Your consumer should only do these five things:

1. Listen to queue

2. Receive message

3. Convert JSON → Event Model

4. Call Handler

5. ACK / NACK

That's it.

Event Flow
Document Service

↓

Publish Event

↓

RabbitMQ

↓

DocumentUploadedConsumer

↓

DocumentUploadedHandler

↓

Business Logic
Pseudo Code
class DocumentUploadedConsumer:

    initialize(handler)

    async start():

        connect to RabbitMQ

        declare exchange

        declare queue

        bind queue

        start consuming

    async on_message(message):

        deserialize message

        validate event

        call handler

        acknowledge message

Very small.

Message Lifecycle
RabbitMQ
     │
     ▼
Receive Message
     │
     ▼
JSON
     │
     ▼
DocumentUploadedEvent
     │
     ▼
Handler.handle(event)
     │
     ▼
Success?

If success:

ACK

If failure:

NACK

↓

RabbitMQ retries
Event Model

The consumer should work with a strongly typed event.

Example:

class DocumentUploadedEvent(BaseModel):

    document_id: UUID

    owner_id: UUID

    storage_path: str

    content_type: str

The consumer should not manually access:

message["document_id"]

Instead:

event = DocumentUploadedEvent.model_validate(data)

This gives automatic validation.

Error Handling

There are two types of errors.

1. Invalid Message

Example:

{
    "abc": 123
}

This isn't a valid event.

Result:

Reject

↓

NACK

↓

Do not process
2. Processing Error

Example:

PDF extraction failed

Result:

NACK

↓

RabbitMQ Retry
Consumer Class

Conceptually:

class DocumentUploadedConsumer:

    def __init__(
        self,
        handler,
        rabbitmq_connection,
    ):
        ...

    async def start(self):
        ...

    async def consume(self, message):
        ...

Notice the consumer depends on abstractions, not implementations.

Consumer vs Handler
Consumer
Receive

↓

Deserialize

↓

Validate

↓

Handler

↓

ACK

Around 30–50 lines of code.

Handler
Download PDF

↓

Extract Text

↓

Chunk

↓

Embeddings

↓

Store

↓

Update Status

Potentially 200+ lines as the project grows.

Worker Startup

Later, your main.py will do something like:

Application Starts

↓

RabbitMQ Connection

↓

Create Consumer

↓

Start Consumer

↓

Wait Forever

This keeps the consumer running continuously.

Phase 2 Checklist
Phase 2 – Consumer

⬜ Create DocumentUploadedConsumer
⬜ Connect to RabbitMQ
⬜ Consume queue
⬜ Validate event
⬜ Call handler
⬜ ACK on success
⬜ NACK on failure
One Improvement I'd Recommend

Since this project will eventually have multiple event types, I wouldn't make the consumer directly responsible for one event forever.

Instead, I'd introduce a small BaseConsumer class later.

BaseConsumer
      ▲
      │
      ├── DocumentUploadedConsumer
      ├── DocumentDeletedConsumer
      ├── EmbeddingFailedConsumer
      └── SearchReindexConsumer

The BaseConsumer would handle all the common RabbitMQ mechanics (connecting, consuming, ACK/NACK), while each specific consumer would only define:

which queue it listens to,
which event model it validates,
which handler it invokes.

That avoids duplicating RabbitMQ code as your event-driven architecture grows. It's a good refactoring once you have two or more consumers.
"""