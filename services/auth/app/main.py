from services.auth.app.api.router import api_router

from shared_lib.core.factory import create_app
from services.auth.app.database.auth_database import Base, engine


app = create_app(
        service_name = "Auth Service",
        router = api_router,
        )