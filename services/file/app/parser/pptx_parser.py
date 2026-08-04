from services.file.app.parser.base_parser import BaseParser

class PptxParser(BaseParser):
    async def extract_text(self, file_path: str) -> str:
            ...