from shared_lib.core.factory import create_app
from services.gateway.app.api.router import api_router

app = create_app(
    service_name="Gateway Service", 
    router=api_router
    )