from datetime import datetime
from pydantic import BaseModel

class HealthResponse(BaseModel):
    service: str
    status: str
    version:  str
    timestamp: datetime