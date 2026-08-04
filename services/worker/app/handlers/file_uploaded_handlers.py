from shared_lib.logger.logger import get_logger

from services.worker.app.clients.file_client import FileClient
from services.worker.app.clients.embedding_client import EmbeddingClient
from services.worker.app.clients.search_client import SearchClient

from services.worker.app.messaging.events import FileUploadedEvent

logger = get_logger(__name__)


class FileUploadedHandler:
    """
    Handles the file.uploaded event.

    Responsibilities:
        - Fetch file metadata
        - Download the file
        - Extract text
        - Chunk text
        - Generate embeddings
        - Store vectors
        - Update file status
    """

    def __init__(
        self,
        file_client: FileClient,
        embedding_client: EmbeddingClient,
        search_client: SearchClient,
    ) -> None:
        self.file_client = file_client()
        self.embedding_client = embedding_client()
        self.search_client = search_client()

    async def handle(
        self,
        event: FileUploadedEvent,
    ) -> None:
        """
        Handle a file.uploaded event.
        """

        logger.info(
            ">>> Processing file %s",
            event.file_id,
        )

        # ----------------------------------
        # Step 1
        # Fetch file metadata
        # ----------------------------------

        file = await self.file_client.get_file(
            file_id=event.file_id,
        )

        logger.info(
            ">>> Fetched metadata for file %s",
            file.file_id,
        )

        # ----------------------------------
        # Step 2
        # Download file
        # (Implement later)
        # ----------------------------------

        file_bytes = await self.file_client.download_file(
            file.file_id,
        )

        logger.info(
            ">>> Fetched bytes for file %s",
            file.file_id,
        )

        # ----------------------------------
        # Step 3
        # Extract text
        # (Implement later)
        # ----------------------------------

        extracted_text = await self.file_client.extract_text(file.file_id,)

        logger.info(
            ">>> Extracted text for file %s",
            file.file_id,
        )

        print(extracted_text)
        # ----------------------------------
        # Step 4
        # Chunk text
        # (Implement later)
        # ----------------------------------

        # chunks = ...

        # ----------------------------------
        # Step 5
        # Generate embeddings
        # (Implement later)
        # ----------------------------------

        # embeddings = await self.embedding_client.generate_embeddings(
        #     chunks
        # )

        # ----------------------------------
        # Step 6
        # Store vectors
        # (Implement later)
        # ----------------------------------

        # await self.search_client.store_vectors(
        #     file.id,
        #     embeddings,
        # )

        # ----------------------------------
        # Step 7
        # Update file status
        # (Implement later)
        # ----------------------------------

        # await self.file_client.update_status(
        #     file.id,
        #     "READY",
        # )

        logger.info(
            "Finished processing file %s",
            event.file_id,
        )