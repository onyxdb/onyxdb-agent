from src.common.base_web_client import BaseWebClient
from src.configs import MdbConfig
from src.mdb.models import UpdateMongoHostsRequest


class MdbClient(BaseWebClient):
    def __init__(self, config: MdbConfig):
        default_headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }
        super().__init__(
            base_url=config.base_url,
            default_headers=default_headers
        )

    async def update_mongo_hosts(self, rq: UpdateMongoHostsRequest):
        await self._put(
            endpoint="/api/managed-mongodb/v1/internal/hosts",
            data=rq.model_dump_json()
        )
