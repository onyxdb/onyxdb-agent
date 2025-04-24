from abc import abstractmethod, ABC

from fastapi import APIRouter


class BaseRouter(ABC):
    def __init__(self, router: APIRouter):
        self._router = router

    @property
    def internal_router(self) -> APIRouter:
        return self._router

    @abstractmethod
    def register_routes(self):
        raise NotImplementedError()
