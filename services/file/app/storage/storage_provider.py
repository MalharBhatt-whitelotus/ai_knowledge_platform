from fastapi import UploadFile
from abc import ABC, abstractmethod


class StorageProvider(ABC):
    """
    Abstract storage provider.

    Every storage backend (Local, S3, Azure, MinIO, etc.)
    must implement these methods.
    """


    @abstractmethod
    async def save(self, file: UploadFile, filename: str,) -> str:
        """
        Save a file.

        Returns:
            str: storage path
        """
        ...


    @abstractmethod
    async def delete(self, path: str) -> None:
        """Delete a stored file."""
        ...


    @abstractmethod
    async def download(self, path: str) -> bytes:
        """
        Download file contents.

        Returns:
            bytes
        """
        ...


    @abstractmethod
    async def exists(self, path: str) -> bool:
        """
        Check whether a file exists.
        """
        ...