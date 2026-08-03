from enum import StrEnum

class ExchangeName(StrEnum):
    DOCUMENT = "document.exchange"

class QueueName(StrEnum):
    DOCUMENT_PROCESSING = "document.processing"

class RoutingKey(StrEnum):
    DOCUMENT_UPLOADED = "document.uploaded"