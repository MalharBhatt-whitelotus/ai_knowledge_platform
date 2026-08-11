from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    [
        "service",
        "method",
        "path",
        "status",
    ],
)


REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    [
        "service",
        "method",
        "path",
    ],
)