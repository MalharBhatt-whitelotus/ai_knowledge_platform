import time
from fastapi import Request
from fastapi.responses import JSONResponse

def register_middleware(app, logger, rate_limiter=None):

    @app.middleware("http")
    async def log_requests(request:Request, call_next):
        start = time.perf_counter()

        if rate_limiter:
            allowed = await rate_limiter.is_allowed(request)
            if not allowed:
                response = JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Too many requests. Please try again later.",
                    },
                )
                duration = (
                    time.perf_counter() - start
                    ) * 1000
                logger.warning(
                    "%s %s | %s | %.2f ms",
                    request.method,
                    request.url.path,
                    response.status_code,
                    duration,
                )

                return response
            
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s | %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
            )
        
        return response