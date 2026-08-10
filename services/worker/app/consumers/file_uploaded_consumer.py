import json
from pydantic import ValidationError
from aio_pika.abc import AbstractIncomingMessage

from shared_lib.enums import DocStatus
from shared_lib.logger.logger import get_logger
from shared_lib.clients.file_client import FileClient

from services.worker.app.messaging.events import FileUploadedEvent


logger = get_logger(__name__)


class FileUploadedConsumer:


    MAX_RETRIES = 3


    def __init__(self, retry_publisher, handler):
        self._retry_publisher = retry_publisher
        self._handler = handler
        self.file_client = FileClient()


    async def consume(self, message: AbstractIncomingMessage) -> None:
        logger.info("🔥 FileUploadedConsumer.consume() called")
        try:
            """
            --------------------------------------------- 
                       * Deserialize message *
            ---------------------------------------------
            """
            payload = json.loads(message.body.decode())

            event = FileUploadedEvent.model_validate(payload)

            logger.info(
                "Received document uploaded event: %s",
                event.file_id,
            )

            """
            ----------------------------
                    * Process Event *
            ----------------------------
            """
            await self._handler.handle(event)

            """
            ----------------
              * Success *
            ----------------
            """
            await message.ack()

            logger.info(
                "Acknowledged message for document %s",
                event.file_id,
            )

        except ValidationError as exc:
            """
            --------------------------------------------- 
                       * Invalid message *
                - Don't retry malformed events. 
            ---------------------------------------------
            """
            logger.exception("Invalid event received: %s", exc)

            # Invalid event → reject permanently
            await self._retry_publisher.publish_dlq(
                body = message.body,
                headers = {
                    **message.headers,
                    "x-error": str(exc),
                    "x-error-type": "ValidationError",
                },
            )
            await message.ack()

        except Exception as exc:
            """
            --------------------------------------------- 
                       * Processing Failure *
            ---------------------------------------------
            """
            retry_count = message.headers.get("x-retry-count", 0)
            logger.exception(
                "Failed to process document event. "
                "retry_count=%s", retry_count
                )

            """
            --------------------------------------------- 
                       * Max Retries reached *
            ---------------------------------------------
            """
            if retry_count >= self.MAX_RETRIES:

                logger.error(
                    "Maximum retries reached. "
                    "Sending message to DLQ."
                )

                await self._retry_publisher.publish_dlq(
                    body=message.body,
                    headers={
                        **message.headers,
                        "x-error": str(exc),
                        "x-error-type": type(exc).__name__,
                    },
                )
                await self.file_client.update_status(
                    event.file_id, DocStatus.rejected.value,
                )

            else:
                logger.warning(
                    "Scheduling message for retry. "
                    "retry_count=%s", retry_count + 1,
                )

                await self._retry_publisher.publish_retry(
                    body=message.body,
                    headers=message.headers,
                    )
            
            """
            --------------------------------------------- 
                    * ACK original message *
                - Already published a retry/DLQ copy.
                - Don't requeue the original message.
            ---------------------------------------------
            """
            await message.ack()