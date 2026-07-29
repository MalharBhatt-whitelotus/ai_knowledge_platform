import uuid
from passlib.context import CryptContext


class AuthUtils:


   pwd_handler = CryptContext(schemes=["bcrypt"], deprecated = "auto")


   """
   ---------------------------------------
     * Check Password Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def check_password(password: str) -> bool:
      has_upper = any(c.isupper() for c in password)
      has_lower = any(c.islower() for c in password)
      has_digit = any(c.isdigit() for c in password)
      has_special = any(not c.isalnum() for c in password)

      return has_upper and has_lower and has_digit and has_special


   """
   ---------------------------------------
     * Hash Password Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def hash_password(password: str) -> str:
      print(password)
      hashed_password = AuthUtils.pwd_handler.hash(password)

      return hashed_password


   """
   ---------------------------------------
    * Verify Password Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def verify_password(password: str, hashed_password: str) -> bool:
      print(password)
      print(hashed_password)
      return AuthUtils.pwd_handler.verify(password, hashed_password)


   """
   ---------------------------------------
        * Get UUID Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def get_uuid() -> str:
      return uuid.uuid4()