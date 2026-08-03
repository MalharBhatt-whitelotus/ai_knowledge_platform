import logging

from services.worker.app.messaging.events import FileUploadedEvent

logger = logging.getLogger(__name__)


class FileUploadedHandler:
    """
    Handles the business workflow for a DocumentUploaded event.

    Responsibilities:
        - Coordinate document processing
        - Delegate work to domain services
        - Raise exceptions on failure so the consumer can NACK the message

    This handler intentionally does NOT contain RabbitMQ logic.
    """

    # def __init__(
    #     self,
    #     storage_provider,
    #     pdf_extractor,
    #     chunking_service,
    #     embedding_service,
    #     document_repository,
    # ):
    #     self._storage_provider = storage_provider
    #     self._pdf_extractor = pdf_extractor
    #     self._chunking_service = chunking_service
    #     self._embedding_service = embedding_service
    #     self._document_repository = document_repository
    
    async def handle(
        self,
        event: FileUploadedEvent,
    ) -> None:
        """
        Process a newly uploaded document.

        Args:
            event: The validated DocumentUploadedEvent.

        Raises:
            Exception:
                Any processing error should propagate so the consumer
                can NACK the message and RabbitMQ can retry.
        """

        logger.info(
            "Processing uploaded document %s",
            event.file_id,
        )

        # -------------------------------------------------------
        # Future phases
        # -------------------------------------------------------

        # 1. Download/read document from storage
        # document = await self._storage_provider.open(event.storage_path)

        # 2. Extract text
        # text = await self._pdf_extractor.extract(document)

        # 3. Split into chunks
        # chunks = await self._chunker.chunk(text)

        # 4. Generate embeddings
        # embeddings = await self._embedding_service.generate(chunks)

        # 5. Persist embeddings
        # await self._embedding_repository.save(
        #     document_id=event.document_id,
        #     embeddings=embeddings,
        # )

        # 6. Update document status
        # await self._document_repository.mark_processed(event.document_id)

        logger.info(
            "Finished processing document %s",
            event.file_id,
        )