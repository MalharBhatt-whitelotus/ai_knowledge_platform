import enum


class DocType(enum.Enum):
    pdf = "pdf"
    txt = "txt"
    docx = "docx"
    xlsx = "xlsx"
    pptx = "pptx"


class DocStatus(enum.Enum):
    in_queue = "in_queue"
    pending = "pending"
    completed = "completed"