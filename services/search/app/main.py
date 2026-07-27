from services.search.app.api.router import api_router

from shared_lib.core.factory import create_app


app = create_app(
        service_name = "Search Service",
        router = api_router,
        )