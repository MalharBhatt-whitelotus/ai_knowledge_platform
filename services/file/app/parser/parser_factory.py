from services.file.app.parser.docx_parser import DocxParser
from services.file.app.parser.pdf_parser import PdfParser
from services.file.app.parser.pptx_parser import PptxParser
from services.file.app.parser.txt_parser import TxtParser
from services.file.app.parser.xlsx_parser import XlsxParser

from shared_lib.enums import DocType

class ParserFactory:

    _parser = {
        DocType.docx.value: DocxParser(),
        DocType.pdf.value: PdfParser(),
        DocType.pptx.value: PptxParser(),
        DocType.txt.value: TxtParser(),
        DocType.xlsx.value: XlsxParser(),
    }

    @classmethod
    def get_parser(cls, content_type: str):
        parser = cls._parser.get(content_type)

        if parser is None:
            raise ValueError(f"Unsupported document type: {content_type}")

        return parser