from shared_lib.app.factory import create_app
from gateway_service.app.api.router import api_router

app = create_app(
    service_name="Gateway Service", 
    router=api_router
    )