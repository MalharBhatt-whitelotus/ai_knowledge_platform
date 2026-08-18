import httpx


class GatewayClient:


    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=5.0,
                read=30.0,
                write=30.0,
                pool=5.0,
        ),
        follow_redirects=True
        )


    async def requests(
            self, 
            method: str, 
            url: str, 
            *,
            headers: dict[str, str] | None = None,
            params: dict | None = None,
            content: bytes | None = None,
            ) -> httpx.Response:

        return await self.client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            content=content,
        )


    async def close(self) -> None:
        await self.client.aclose()