import asyncio
import logging
from typing import List

import uvicorn
from fastapi import FastAPI

from src.common.logging import DisabledEndpointFilter
from src.configs import HttpConfig
from src.http.routers.base_router import BaseRouter
from src.http.routers.internal_router import InternalRouter
from src.http.routers.mongo_router import MongoRouter
from src.mdb.mongo_service import MongoService

logger = logging.getLogger(__name__)


class HttpService:
    def __init__(self,
                 config: HttpConfig,
                 mongo_service: MongoService):
        self._app = FastAPI()
        self._config = config
        self._mongo_service = mongo_service

    def run(self):
        self._add_middlewares(self._app)
        HttpService.register_routers(self._app, self._get_routers())
        config = uvicorn.Config(self._app,
                                host=self._config.host,
                                port=self._config.port,
                                log_level="info",
                                log_config=None)
        server = uvicorn.Server(config)
        self._add_logger_filters()
        asyncio.run(server.serve())

    def _get_routers(self) -> List[BaseRouter]:
        return [
            InternalRouter(),
            MongoRouter(self._mongo_service)
        ]

    @staticmethod
    def register_routers(app: FastAPI, routers: List[BaseRouter]):
        for router in routers:
            router.register_routes()
            app.include_router(router.internal_router)

    @staticmethod
    def _add_logger_filters():
        uvicorn_logger = logging.getLogger("uvicorn.access")
        uvicorn_logger.addFilter(DisabledEndpointFilter(path=InternalRouter.ROUTER_PREFIX))

    @staticmethod
    def _add_middlewares(app: FastAPI):
        pass
    #     app.add_middleware(ExceptionHandlerMiddleware)
