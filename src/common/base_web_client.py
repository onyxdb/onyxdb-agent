import logging
from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator

import aiohttp
import requests

from src.common import methods

logger = logging.getLogger(__name__)


class BasePaginator(ABC):
    @abstractmethod
    async def get_next_page_url(self, response: aiohttp.ClientResponse, base_url: str) -> Optional[str]:
        raise NotImplementedError()


class BaseWebClient:
    _LOG_PREFIX = "BaseWebClient"
    _METHODS = {
        "GET": aiohttp.ClientSession.get,
        "POST": aiohttp.ClientSession.post,
        "PUT": aiohttp.ClientSession.put,
        "DELETE": aiohttp.ClientSession.delete,
    }

    def __init__(self,
                 base_url: Optional[str] = None,
                 auth_headers: Optional[dict] = None,
                 default_headers: Optional[dict] = None,
                 verify: bool = True,
                 paginator: Optional[BasePaginator] = None,
                 proxy: Optional[str] = None,
                 timeout: int = 10):
        self._base_url = base_url
        self._auth_headers = auth_headers or {}
        self._default_headers = default_headers or {}
        self._verify = verify
        self._paginator = paginator
        self._proxy = proxy
        self._timeout = timeout

    async def _get_json(self, endpoint: Optional[str] = None, **kwargs) -> dict:
        return await (await self._get(endpoint=endpoint, **kwargs)).json()

    async def _get(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request_single(method="GET", endpoint=endpoint, **kwargs)

    async def _get_yield_json(self, endpoint: str, **kwargs) -> AsyncIterator[aiohttp.ClientResponse]:
        async for response in await self._get_yield(endpoint, **kwargs):
            yield await response.json()

    async def _get_yield(self, endpoint: str, **kwargs) -> AsyncIterator[aiohttp.ClientResponse]:
        return self._request(method="GET", endpoint=endpoint, **kwargs)

    async def _post_json(self, endpoint: str, **kwargs) -> dict:
        return await (await self._post(endpoint=endpoint, **kwargs)).json()

    async def _put_json(self, endpoint: str, **kwargs) -> dict:
        return await (await self._put(endpoint=endpoint, **kwargs)).json()

    async def _post(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request_single(method="POST", endpoint=endpoint, **kwargs)

    async def _put(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request_single(method="PUT", endpoint=endpoint, **kwargs)

    async def _request_single(self, *args, **kwargs) -> aiohttp.ClientResponse:
        return await self._request(*args, **kwargs).__anext__()

    async def _request(self,
                       method: str,
                       endpoint: Optional[str] = None,
                       base_url: Optional[str] = None,
                       headers: Optional[dict] = None,
                       verify: Optional[bool] = None,
                       paginator: Optional[BasePaginator] = None,
                       proxy: Optional[str] = None,
                       timeout: Optional[int] = None,
                       secured_response: bool = True,
                       **kwargs) -> AsyncIterator[aiohttp.ClientResponse]:
        rq_base_url = self._base_url if base_url is None else base_url
        rq_url = rq_base_url + endpoint if endpoint is not None else rq_base_url
        rq_verify = self._verify or verify
        rq_paginator = self._paginator or paginator
        rq_proxy = self._proxy or proxy
        rq_timeout = timeout if timeout else self._timeout

        rq_headers = {}
        rq_headers.update(self._auth_headers)
        if headers:
            rq_headers.update(headers)
        else:
            rq_headers.update(self._default_headers)

        connector = aiohttp.TCPConnector(verify_ssl=rq_verify)
        async with aiohttp.ClientSession(connector=connector) as session:
            while rq_url:
                response: aiohttp.ClientResponse = await BaseWebClient._METHODS[method](session,
                                                                                        rq_url,
                                                                                        headers=rq_headers,
                                                                                        proxy=rq_proxy,
                                                                                        timeout=rq_timeout,
                                                                                        **kwargs)
                # if secured_response:
                #     logger.info(f"status={response.status}")
                # else:
                #     response_text = await response.text()
                #     logger.info(f"status={response.status}; response_text={response_text}")
                response.raise_for_status()
                yield response
                if not rq_paginator:
                    break

                rq_url = await rq_paginator.get_next_page_url(response, rq_base_url)

    @staticmethod
    def raise_for_status(response: requests.models.Response):
        """
        Copy of requests.models.Response.raise_for_status, but it doesn't show request url
        """

        http_error_msg = ''
        if isinstance(response.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = response.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = response.reason.decode('iso-8859-1')
        else:
            reason = response.reason

        if 400 <= response.status_code < 500:
            http_error_msg = u'%s Client Error: %s' % (response.status_code, reason)

        elif 500 <= response.status_code < 600:
            http_error_msg = u'%s Server Error: %s' % (response.status_code, reason)

        if http_error_msg:
            raise requests.exceptions.HTTPError(http_error_msg, response=response)

    @staticmethod
    def _make_payload(base_payload: Optional[dict] = None, **optional_payload):
        return methods.add_optionals_to_dict(base_payload, **optional_payload)
