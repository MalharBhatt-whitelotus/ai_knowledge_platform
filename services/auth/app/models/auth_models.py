from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum

from services.auth.app.database.auth_database import Base
from services.auth.app.enums import Role, DocType

class UserAuthenticationDetail(Base):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False, unique=True, index=True)
    role = Column(Enum(Role), nullable=False)
    # role = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    #new column
    doc_id = Column(String, unique=True, index=True)
    doc_type = Column(Enum(DocType))