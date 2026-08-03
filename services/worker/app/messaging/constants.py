from enum import StrEnum

class ExchangeName(StrEnum):
    FILE = "file.exchange"

class QueueName(StrEnum):
    FILE_PROCESSING = "file.processing"

class RoutingKey(StrEnum):
    FILE_UPLOADED = "file.uploaded"