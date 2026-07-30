import enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"

class DocType(enum.Enum):
    pdf = "pdf"
    txt = "txt"
