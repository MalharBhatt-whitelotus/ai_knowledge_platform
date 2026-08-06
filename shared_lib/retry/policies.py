import httpx
from tenacity import retry_if_exception_type, stop_after_attempt, wait_exponential


HTTP_RETRY_POLICY = {
    "retry": retry_if_exception_type(
        (
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.NetworkError,
        )
    ),
    "stop": stop_after_attempt(3),
    "wait": wait_exponential(
        multiplier=1,
        min=1,
        max=8,
    ),
    "reraise": True,
}