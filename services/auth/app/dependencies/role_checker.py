"""
CLASS RoleChecker

    FUNCTION initialize(allowed_roles)
        STORE allowed_roles
    END FUNCTION


    FUNCTION call(current_user)

        # Check if the user's role is allowed
        IF current_user.role IS NOT IN allowed_roles THEN

            RAISE HTTP 403 Forbidden
                MESSAGE = "You do not have permission to perform this action."

        END IF

        # User is authorized
        RETURN current_user

    END FUNCTION

END CLASS
"""
from fastapi import Depends, HTTPException, status

from services.auth.app.models.auth_models import Role
from services.auth.app.schemas.auth_schemas import CurrentUserResponse
from services.auth.app.dependencies.current_user import get_current_user
class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        self.allowed_role = allowed_roles

    def __call__(self, current_user: CurrentUserResponse = Depends(get_current_user)) -> CurrentUserResponse:
        try:
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User.")

            if current_user.role.value not in self.allowed_role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not allowed.")

            return current_user
        
        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

admin_only = RoleChecker([Role.admin.value])
user_only = RoleChecker([Role.user.value])
user_or_admin = RoleChecker([Role.user.value, Role.admin.value])