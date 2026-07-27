from fastapi import Request
from fastapi.responses import JSONResponse

from shared_lib.exceptions.exceptions import AppException
from shared_lib.schemas.error import ErrorDetail, ErrorResponse

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                service=request.app.title
            )
        ).model_dump(),
    )