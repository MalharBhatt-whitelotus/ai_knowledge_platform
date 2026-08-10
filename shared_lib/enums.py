import enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"

class DocType(enum.Enum):
    pdf = "pdf"
    txt = "txt"
    docx = "docx"
    xlsx = "xlsx"
    pptx = "pptx"


class DocStatus(enum.Enum):
    in_queue = "in_queue"
    ready_for_processing = "ready_for_processing"
    completed = "completed"
    rejected = "rejected"