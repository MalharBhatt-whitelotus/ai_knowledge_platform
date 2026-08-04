import fitz

from services.file.app.parser.base_parser import BaseParser

class PdfParser(BaseParser):

    async def extract_text(self, file_path: str) -> str:
        pdf = fitz.open(file_path)
        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()
        return text