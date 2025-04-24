import asyncio
import logging
import threading
import time
from typing import List, Dict, Any

from pymongo import MongoClient
from pymongo.synchronous.database import Database

from src.configs import AgentConfig
from src.http.http_service import HttpService
from src.mdb.mdb_client import MdbClient
from src.mdb.models import MongoHost, UpdateMongoHostsRequest, MongoHostType, MongoHostStatus, MongoHostRole
from src.mdb.mongo_service import MongoService

logger = logging.getLogger(__name__)


class Agent:
    _REPORT_HOSTS_DELAY_SECONDS = 5

    def __init__(self, config: AgentConfig):
        self._config = config
        self._mongo_client = MongoClient(config.mongo.uri)
        self._mdb_client = MdbClient(config.mdb)
        self._mongo_service = MongoService(self._mongo_client)
        self._http_service = HttpService(
            config=config.http,
            mongo_service=self._mongo_service
        )

    def start(self):
        asyncio.run(self.async_start())

    async def async_start(self):
        http_service_process = threading.Thread(target=self._http_service.run)
        http_service_process.start()

        admin_db = self._mongo_client.get_database("admin")

        logger.info(f"Started reporting hosts for cluster_id={self._config.mdb.cluster_id}")
        while True:
            try:
                await self._report_hosts(admin_db)
                logger.info(f"Reported hosts for cluster_id={self._config.mdb.cluster_id}")
            except Exception as e:
                logger.error(f"Failed to report hosts", e)
            time.sleep(self._REPORT_HOSTS_DELAY_SECONDS)

    async def _report_hosts(self, admin_db: Database):
        hosts: List[MongoHost] = await self._get_rs_hosts(admin_db)
        await self._mdb_client.update_mongo_hosts(UpdateMongoHostsRequest(
            hosts=hosts
        ))

    async def _get_rs_hosts(self, admin_db: Database) -> List[MongoHost]:
        rs_status = admin_db.command("replSetGetStatus")
        members = rs_status.get("members", [])

        return [self._parse_rs_member(member) for member in members]

    def _parse_rs_member(self, member: Dict[str, Any]) -> MongoHost:
        health = int(member.get("health", 0))
        state = int(member.get("state", 6))

        status = MongoHostStatus.alive if health == 1 else MongoHostStatus.dead
        role = MongoHostRole.unknown
        if state == 1:
            role = MongoHostRole.primary
        elif state == 2:
            role = MongoHostRole.secondary

        return MongoHost(
            name=str(member.get("name")).split(".")[0],
            clusterId=self._config.mdb.cluster_id,
            type=MongoHostType.mongod,
            status=status,
            role=role
        )
