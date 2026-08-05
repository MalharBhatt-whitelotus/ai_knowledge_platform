from sentence_transformers import SentenceTransformer
from fastapi import HTTPException, status

from shared_lib.logger.logger import get_logger


class EmbeddingService:


    def __init__(self) -> None:
        self.model : SentenceTransformer | None = None
        self.logger = get_logger(__name__)


    def load_model(self) -> None:
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")


    async def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        try:
            if self.model is None:
                raise RuntimeError("Embedding model is not loaded.")

            if not chunks:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Empty chunks are not allowed")

            embeddings = self.model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True,)
            if embeddings is None or len(embeddings) == 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unable to create embeddings.")
            
            return embeddings.tolist()

        except HTTPException:
            raise

        except RuntimeError as r_exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(r_exc))

        except Exception as exc:
            self.logger.error(">>> %s",exc)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))