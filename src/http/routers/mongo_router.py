from fastapi import APIRouter, Body, Response

from src.http.models.mongo_models import CreateMongoDatabaseRequest, DeleteMongoDatabaseRequest
from src.http.routers.base_router import BaseRouter
from src.mdb.mongo_service import MongoService


class MongoRouter(BaseRouter):
    ROUTER_PREFIX = "/api/mongodb"

    def __init__(self, mongo_service: MongoService):
        super().__init__(router=APIRouter(prefix=self.ROUTER_PREFIX, tags=["MongoDB"]))
        self._mongo_service = mongo_service

    def register_routes(self):
        self._router.post(
            path="/databases",
            summary="Create MongoDB database"
        )(self._create_database)
        self._router.delete(
            path="/databases",
            summary="Delete MongoDB database"
        )(self._delete_database)

    async def _create_database(self, rq: CreateMongoDatabaseRequest = Body()):
        await self._mongo_service.create_database(rq.name)
        return Response()

    async def _delete_database(self, rq: DeleteMongoDatabaseRequest = Body()):
        await self._mongo_service.delete_database(rq.name)
        return Response()