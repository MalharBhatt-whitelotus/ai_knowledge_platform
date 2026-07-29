import uuid
from passlib.context import CryptContext
class AuthUtils:


    pwd_handler = CryptContext(schemes=["bcrypt"], deprecated = "auto")


    @staticmethod
    def check_password(password: str) -> bool:
       has_upper = any(c.isupper() for c in password)
       has_lower = any(c.islower() for c in password)
       has_digit = any(c.isdigit() for c in password)
       has_special = any(not c.isalnum() for c in password)

       return has_upper and has_lower and has_digit and has_special


    @staticmethod
    def hash_password(password: str) -> str:
       hashed_password = AuthUtils.pwd_handler.hash(password)
       return hashed_password


    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
       return AuthUtils.pwd_handler.verify(password, hashed_password)

    @staticmethod
    def get_uuid() -> str:
       return uuid.uuid4()