from pathlib import Path
from fastapi import UploadFile

from services.file.app.storage.storage_provider import StorageProvider

class LocalStorage(StorageProvider):

    def __init__(self, upload_directory: str) -> None:
        self.upload_dir = Path(upload_directory)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


    """
    -------------------------------------
            * Save File Function * 
    -------------------------------------
    """
    async def save(self, file: UploadFile, filename: str) -> str:
        destination = self.upload_dir/filename

        with open(destination, "wb") as buffer:
            buffer.write(await file.read())

        return str(destination)


    """
    -------------------------------------
            * Save File Function * 
    -------------------------------------
    """
    async def delete(self, path: str) -> None:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(path)

        file_path.unlink()