from fastapi import Depends, HTTPException, status

from services.file.app.enums import Role
from services.file.app.schemas.auth_schemas import CurrentUserResponse
from services.file.app.clients.auth_client import auth_client


class RoleChecker:


    def __init__(self, allowed_roles: list[str]):
        self.allowed_role = allowed_roles


    def __call__(self, current_user: CurrentUserResponse = Depends(auth_client.get_current_user)) -> CurrentUserResponse:
        try:
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User.")

            if current_user.role not in self.allowed_role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not allowed.")

            return current_user
        
        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


admin_only = RoleChecker([Role.admin.value])
user_only = RoleChecker([Role.user.value])
user_or_admin = RoleChecker([Role.user.value, Role.admin.value])