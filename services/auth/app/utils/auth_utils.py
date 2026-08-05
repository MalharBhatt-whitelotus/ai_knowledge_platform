import uuid
from pwdlib import PasswordHash
from shared_lib.logger.logger import get_logger

class AuthUtils:


   pwd_handler = PasswordHash.recommended()


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
      return AuthUtils.pwd_handler.hash(password)


   """
   ---------------------------------------
    * Verify Password Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def verify_password(password: str, hashed_password: str) -> bool:
      return AuthUtils.pwd_handler.verify(password, hashed_password)


   """
   ---------------------------------------
        * Get UUID Utility Function *
   ---------------------------------------
   """
   @staticmethod
   def get_uuid() -> str:
      return str(uuid.uuid4())