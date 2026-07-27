from services.embedding.app.api.router import api_router

from shared_lib.core.factory import create_app


app = create_app(
        service_name = "Embedding Service",
        router = api_router,
        )