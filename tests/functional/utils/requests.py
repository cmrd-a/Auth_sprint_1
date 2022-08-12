from dataclasses import dataclass

from multidict import CIMultiDictProxy

from settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


async def http_get_request(http_session, method: str, params: dict | None) -> HTTPResponse:
    params = params or {}
    url = f"{settings.service_url}/api{method}"
    async with http_session.get(url, params=params) as response:
        return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
        )
