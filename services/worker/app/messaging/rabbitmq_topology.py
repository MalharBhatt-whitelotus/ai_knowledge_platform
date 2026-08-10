from aio_pika import ExchangeType

from services.worker.app.messaging.rabbitmq import RabbitMQConnection


class RabbitmqTopology:

    MAIN_EXCHANGE = "files"
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

    async def setup(self, rabbitmq: RabbitMQConnection):

        main_exchange = await rabbitmq.declare_exchange(
            exchange_name=self.MAIN_EXCHANGE, 
            exchange_type=ExchangeType.DIRECT,
            )
        
        retry_exchange = await rabbitmq.declare_exchange(
            exchange_name=self.RETRY_EXCHANGE, 
            exchange_type=ExchangeType.DIRECT,
            )
        
        dlq_exchange = await rabbitmq.declare_exchange(
            exchange_name=self.DLQ_EXCHANGE, 
            exchange_type=ExchangeType.DIRECT,
            )

        main_queue = await rabbitmq.declare_queue(
            queue_name=self.MAIN_QUEUE,
            exchange=main_exchange, 
            routing_key=self.ROUTING_KEY
            )

        retry_queue = await rabbitmq.declare_queue(
            queue_name=self.RETRY_QUEUE,
            exchange=retry_exchange,
            routing_key=self.RETRY_ROUTING_KEY, 
            arguments={
            "x-message-ttl": self.RETRY_TTL,
            "x-dead-letter-exchange": self.MAIN_EXCHANGE,
            "x-dead-letter-routing-key": self.ROUTING_KEY,
        },
        )

        dlq_queue = await rabbitmq.declare_queue(
            queue_name=self.DLQ_QUEUE,
            exchange=dlq_exchange,
            routing_key=self.DLQ_ROUTING_KEY,
            )

        return{
            "main_exchange": main_exchange,
            "retry_exchange": retry_exchange,
            "dlq_exchange": dlq_exchange,
            "main_queue": main_queue,
            "retry_queue": retry_queue,
            "dlq_queue": dlq_queue
        }