from shared_lib.core.factory import create_app
from services.gateway_service.app.api.router import api_router

app = create_app(
    service_name="Gateway Service", 
    router=api_router
    )

from shared_lib.exceptions.exceptions import AppException

@app.get("/test-error")
async def test_error():
    raise AppException(code="TEST ERROR", message="Testing Excption Handling.",status_code=400,)