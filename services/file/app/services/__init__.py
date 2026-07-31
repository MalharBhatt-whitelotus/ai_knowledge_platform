"""
import uuid

from fastapi import UploadFile

from app.storage.base import StorageProvider


class DocumentService:

    def __init__(
        self,
        repository,
        storage_provider: StorageProvider,
        publisher,
    ):
        self.repository = repository
        self.storage = storage_provider
        self.publisher = publisher

    async def upload_document(
        self,
        file: UploadFile,
    ):

        # Validation
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files are allowed.")

        filename = f"{uuid.uuid4()}.pdf"

        storage_path = await self.storage.save(
            file=file,
            filename=filename,
        )

        document = await self.repository.create_document(
            filename=file.filename,
            storage_path=storage_path,
        )

        await self.publisher.publish_document_uploaded(
            document.id
        )

        return document

        
    async def delete_document(
        self,
        document_id: str,
    ):

    document = await self.repository.get(document_id)

    if document is None:
        raise ValueError("Document not found.")

    if not await self.storage.exists(document.storage_path):
        raise FileNotFoundError()

    await self.storage.delete(document.storage_path)

    await self.repository.delete(document_id)

async def download_document(
    self,
    document_id: str,
):

    document = await self.repository.get(document_id)

    if document is None:
        raise ValueError("Document not found.")

    if not await self.storage.exists(document.storage_path):
        raise FileNotFoundError()

    return await self.storage.download(
        document.storage_path
    )
        
        """