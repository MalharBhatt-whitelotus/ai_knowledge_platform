from docx import Document

from services.file.app.parser.base_parser import BaseParser

class DocxParser(BaseParser):
    async def extract_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            document = Document(file_path)
            text = "\n".join(
                paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()
                )    
        return text