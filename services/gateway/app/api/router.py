from fastapi import APIRouter, Request

from services.gateway.app.config.config import settings

SERVICE_URLS = {
    "auth": settings.auth_service_url,
    "file": settings.file_service_url,
    "embedding": settings.embedding_service_url,
    "search": settings.search_service_url,
    "ai": settings.ai_service_url,
}

api_router = APIRouter()

@api_router.api_route(
    "/proxy/{service}/{path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ],
)
async def proxy(service: str, path: str, request: Request,):

    base_url = SERVICE_URLS.get(service)

    if base_url is None:
        return {"detail": f"Unknown service: {service}"}

    target_url = f"{base_url.rstrip('/')}/{path}"

    gateway_proxy = request.app.state.gateway_proxy

    return await gateway_proxy.forward(
        request=request,
        target_url=target_url,
    )