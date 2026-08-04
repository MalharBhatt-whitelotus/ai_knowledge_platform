from abc import ABC, abstractmethod

class BaseParser(ABC):

    @abstractmethod
    async def extract_text(self, file_path: str) -> str:
        """
        Extract text from the document.
        """
        pass