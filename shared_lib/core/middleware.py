import time
from fastapi import Request
from fastapi.responses import JSONResponse

from shared_lib.observability.metrics import REQUEST_COUNT, REQUEST_DURATION

def register_middleware(app, logger, service_name: str, rate_limiter=None):

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

                REQUEST_COUNT.labels(
                    service=service_name,
                    method=request.method,
                    path=request.url.path,
                    status=str(response.status_code),
                ).inc()

                REQUEST_DURATION.labels(
                    service=service_name,
                    method=request.method,
                    path=request.url.path,
                ).observe(duration)

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

        REQUEST_COUNT.labels(
            service=service_name,
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).inc()

        REQUEST_DURATION.labels(
            service=service_name,
            method=request.method,
            path=request.url.path,
        ).observe(duration)
        
        logger.info(
            "%s %s | %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
            )
        
        return response