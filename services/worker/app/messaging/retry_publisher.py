from aio_pika import Message

class RetryPublisher:

    RETRY_ROUTING_KEY = "file.uploaded.retry"
    DLQ_ROUTING_KEY = "file.uploaded.dlq"

    def __init__(self, retry_exchange, dlq_exchange):
        self.retry_exchange = retry_exchange
        self.dlq_exchange = dlq_exchange

    async def publish_retry(self, body: bytes, headers: dict):
        retry_count = headers.get("x-retry-count", 0)
        retry_count += 1

        new_headers = {
            **headers,
            "x-retry-count": retry_count
        }

        message = Message(body=body, headers=new_headers, delivery_mode=2)

        await self.retry_exchange.publish(message, routing_key=self.RETRY_ROUTING_KEY)

    async def publish_dlq(self, body: bytes, headers: dict):
        message = Message(body=body, headers=headers, delivery_mode=2)
        await self.dlq_exchange.publish(message, self.DLQ_ROUTING_KEY)