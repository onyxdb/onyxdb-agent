from fastapi import APIRouter

from src.http.routers.base_router import BaseRouter


class InternalRouter(BaseRouter):
    ROUTER_PREFIX = "/api/internal"

    def __init__(self):
        super().__init__(router=APIRouter(prefix=self.ROUTER_PREFIX, tags=["Internal"]))

    def register_routes(self):
        self._router.get("/ping")(self._ping)

    async def _ping(self) -> str:
        return "pong"
