from abc import ABC, abstractmethod

class BaseChunker(ABC):

    @abstractmethod
    async def chunk(self, extract_text: str) -> list[str]:
        pass 