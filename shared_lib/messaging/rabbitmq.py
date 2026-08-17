import aio_pika
from aio_pika import Channel, Connection, Exchange, ExchangeType, Queue


class RabbitMQConnection:


    def __init__(self, rabbitmq_url: str):
       self.rabbitmq_url = rabbitmq_url
       self.channel: Channel | None = None
       self.connection: Connection | None = None


    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(
            prefetch_count=10
        )
        return self.channel


    async def declare_exchange(
            self, 
            exchange_name: str, 
            exchange_type: ExchangeType = ExchangeType.DIRECT,
            ) -> Exchange:
        if self.channel is None: 
            raise RuntimeError(
                "RabbitMQ channel is not initialized. " 
                "Call connect() first."
                )

        return await self.channel.declare_exchange(
            name=exchange_name, 
            type=exchange_type, 
            durable=True,
            )


    async def declare_queue(
            self,
            queue_name: str, 
            exchange: Exchange, 
            routing_key: str,
            arguments: dict | None = None
            ) -> Queue:

        if self.channel is None: 
            raise RuntimeError(
                "RabbitMQ channel is not initialized. "
                "Call connect() first."
                )

        queue = await self.channel.declare_queue(
            name=queue_name, 
            durable=True,
            arguments=arguments,
            )
        
        await queue.bind(
            exchange=exchange, 
            routing_key=routing_key
                    )

        return queue


    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None 