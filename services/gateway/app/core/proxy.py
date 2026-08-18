import httpx
from fastapi import Request
from fastapi.responses import Response

class GatewayProxy:

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=5.0,
                read=30.0,
                write=30.0,
                pool=5.0,
            ),
            follow_redirects=True,
        )

    async def forward(
            self,
            request: Request,
            target_url: str,
    ) -> Response:

        body = await request.body()

        headers = dict(request.headers)

        headers.pop("host", None)

        try:
            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=body,
            )

        except httpx.ConnectError:
            return Response(
                content='{"detail": "Downstream service unavailable"}',
                status_code=503,
                media_type="application/json",
            )

        except httpx.TimeoutException:
            return Response(
                content='{"detail": "Downstream service timeout"}',
                status_code=504,
                media_type="application/json",
            )

        response_headers = {
            key: value
            for key, value in response.headers.items()
            if key.lower() not in {
                "content-length",
                "transfer-encoding",
                "connection",
                "content-encoding",
            }
        }

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers,
        )

    async def close(self) -> None:
        await self.client.aclose()