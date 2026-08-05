from services.file.app.parser.base_parser import BaseParser

class TxtParser(BaseParser):
    async def extract_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        return text