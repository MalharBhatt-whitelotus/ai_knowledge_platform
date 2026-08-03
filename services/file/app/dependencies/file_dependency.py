from pathlib import Path
from fastapi import Request

from services.file.app.storage.local_storage import LocalStorage
from services.file.app.services.file_services import FileServices
from services.file.app.repositories.file_repository import FileRepository as repo


directory = Path(__file__).resolve().parent.parent.parent


def get_file_service(request: Request):
    storage = LocalStorage(f"{directory}/saved_files")
    services = FileServices(
        repository=repo,
        storage_provider=storage,
        publisher=request.app.state.publisher,
        )

    return services