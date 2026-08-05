from services.search.app.database.chroma import collection
from services.search.app.services.search_service import SearchService
from services.search.app.repositories.chroma_repository import ChromaRepository

repository = ChromaRepository(collection=collection)
service = SearchService(repo=repository)