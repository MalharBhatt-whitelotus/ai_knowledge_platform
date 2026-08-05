import json
import logging
from aio_pika import Exchange, Message

from shared_lib.logger.logger import get_logger
from services.worker.app.messaging.events import FileUploadedEvent

logger = get_logger(__name__)

class RabbitMQPublisher:

    ROUTING_KEY = "file.uploaded"

    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    async def publish_file_uploaded(self, event: FileUploadedEvent) -> None:
        try:

            logger.info(">>> publish_file_uploaded called")
            logger.info(f">>> {event}")
            message = Message(
                body=event.model_dump_json().encode("utf-8"),
                content_type="application/json"
                )
            await self.exchange.publish(message, routing_key=self.ROUTING_KEY,)
            logger.info(">>> message published")
        except Exception as e:
            logger.exception("Failed to publish RabbitMQ message")
            raise