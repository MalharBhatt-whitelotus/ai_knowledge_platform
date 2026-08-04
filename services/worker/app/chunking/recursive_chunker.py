from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.worker.app.chunking.base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            )

    async def chunk(self, text: str) -> list[str]:
        return self.splitter.split_text(text)