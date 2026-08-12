from prometheus_client import start_http_server


def start_metrics_server(
    port: int = 9000,
):
    start_http_server(port)