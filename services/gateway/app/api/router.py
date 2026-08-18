from fastapi import APIRouter, Request

from services.gateway.app.config.config import settings


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
    service_urls = {
        "auth": settings.ai_service_url,
        "file": settings.file_service_url,
        "ai": settings.ai_service_url,
    }

    base_url = service_urls.get(service)

    if base_url is None:
        return {"detail": f"Unknown service: {service}"}

    target_url = f"{base_url.rstrip('/')}/{path}"

    gateway_proxy = request.app.state.gateway_proxy

    return await gateway_proxy.forward(
        request=request,
        target_url=target_url,
    )