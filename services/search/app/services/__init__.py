from services.search.app.database.chroma import collection
from services.search.app.services.search_service import SearchService
from services.search.app.clients.embedding_client import EmbeddingClient
from services.search.app.repositories.chroma_repository import ChromaRepository

embedding_client = EmbeddingClient()
repository = ChromaRepository(collection=collection)
service = SearchService(repo=repository, embedding_client=embedding_client)
