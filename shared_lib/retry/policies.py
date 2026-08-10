import httpx
from tenacity import retry_if_exception_type, stop_after_attempt, wait_exponential

from shared_lib.config.settings import settings

HTTP_RETRY_POLICY = {
    "retry": retry_if_exception_type(
        (
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.NetworkError,
        )
    ),
    "stop": stop_after_attempt(settings.RETRY_ATTEMPTS),
    "wait": wait_exponential(
        multiplier=2,
        min=settings.RETRY_MIN_WAIT,
        max=settings.RETRY_MAX_WAIT,
    ),
    "reraise": True,
}