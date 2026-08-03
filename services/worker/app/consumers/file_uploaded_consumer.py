import json
from shared_lib.logger.logger import get_logger
from pydantic import ValidationError
from aio_pika.abc import AbstractIncomingMessage

from services.worker.app.messaging.events import FileUploadedEvent

logger = get_logger(__name__)

class FileUploadedConsumer:

    def __init__(self, rabbitmq, handler):
        self._rabbitmq = rabbitmq
        self._handler = handler

    async def consume(self, message: AbstractIncomingMessage) -> None:
        try:
            payload = json.loads(message.body.decode())

            event = FileUploadedEvent.model_validate(payload)

            logger.info(
                "Received document uploaded event: %s",
                event.file_id,
            )

            await self._handler.handle(event)

            await message.ack()

            logger.info(
                "Acknowledged message for document %s",
                event.file_id,
            )

        except ValidationError as exc:
            logger.exception("Invalid event received: %s", exc)

            # Invalid event → reject permanently
            await message.reject(requeue=False)

        except Exception as exc:
            logger.exception("Failed to process document event")

            # Processing failure → retry later
            await message.nack(requeue=True)

    async def start_listening(self) -> None:
        logger.info("Consumer is listening...")
        await self._rabbitmq.consume(queue_name="file.uploaded", callback=self.consume,)