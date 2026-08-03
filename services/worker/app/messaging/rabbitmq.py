import aio_pika
from aio_pika import Channel, Connection, Exchange, ExchangeType


class RabbitMQConnection:


    def __init__(self, rabbitmq_url: str):
       self.rabbitmq_url = rabbitmq_url
       self.channel: Channel | None = None
       self.connection: Connection | None = None
       self.exchange: Exchange | None = None


    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()


    async def declare_exchange(
            self, 
            exchange_name: str, 
            exchange_type: ExchangeType = ExchangeType.DIRECT,
            ) -> Exchange:
        self.exchange = await self.channel.declare_exchange(
            exchange_name, exchange_type, durable=True,
            )
        return self.exchange


    async def declare_queue(self, queue_name: str, routing_key: str):

        queue = await self.channel.declare_queue(name=queue_name, durable=True)
        await queue.bind(exchange=self.exchange, routing_key=routing_key)

        return queue


    async def close(self):
        if self.connection:
            await self.connection.close()