import logging
from tenacity import retry, before_sleep_log


from shared_lib.logger.logger import get_logger
from shared_lib.retry.policies import HTTP_RETRY_POLICY

logger = get_logger(__name__)
http_retry = retry(
    before_sleep=before_sleep_log(logger,log_level=logging.WARNING),
    **HTTP_RETRY_POLICY,
    )