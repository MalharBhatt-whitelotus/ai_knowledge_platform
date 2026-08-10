from aio_pika import ExchangeType

class RabbitmqTopology:

    MAIN_EXCHANGE = "file_events_exchange"
    RETRY_EXCHANGE = "file_events_retry_exchange"
    DLQ_EXCHANGE = "file_event_dlq_exchange"

    MAIN_QUEUE = "file_uploaded_queue"
    RETRY_QUEUE = "file_uploaded_retry_queue"
    DLQ_QUEUE = "file_uploaded_dlq"

    ROUTING_KEY = "file.uploaded"
    RETRY_ROUTING_KEY = "file.uploaded.retry"
    DLQ_ROUTING_KEY = "file.uploaded.dlq"

    RETRY_TTL = 5000
    MAX_RETRIES = 3

    async def setup(self, channel):

        main_exchange = await channel.declare_exchange(self.MAIN_EXCHANGE, ExchangeType.DIRECT, durable=True)
        retry_exchange = await channel.declare_exchange(self.RETRY_EXCHANGE, ExchangeType.DIRECT, durable=True)
        dlq_exchange = await channel.declare_exchange(self.DLQ_EXCHANGE, ExchangeType.DIRECT, durable=True)

        main_queue = await channel.declare_queue(self.MAIN_QUEUE, durable=True)
        await main_queue.bind(main_exchange, routing_key=self.ROUTING_KEY)

        retry_queue = await channel.declare_queue(self.RETRY_QUEUE, durable=True, arguments={
            "x-message-ttl": self.RETRY_TTL,
            "x-dead-letter-exchange": self.MAIN_EXCHANGE,
            "x-dead-letter-routing-key": self.ROUTING_KEY,
        })
        await retry_queue.bind(retry_exchange, routing_key=self.RETRY_ROUTING_KEY)

        dlq_queue = await channel.declare_queue(self.DLQ_QUEUE, durable=True)
        await dlq_queue.binf(dlq_exchange, routing_key=self.DLQ_ROUTING_KEY)

        return{
            "main_exchange": main_exchange,
            "retry_exchange": retry_exchange,
            "dlq_exchange": dlq_exchange,
            "main_queue": main_queue,
            "retry_queue": retry_queue,
            "dlq_queue": dlq_queue
        }