import base64
import logging

from kubernetes import client
from pymongo import MongoClient

from src.http.models.mongo_models import CreateMongoUserRequestDTO, DeleteMongoUserRequestDTO

logger = logging.getLogger(__name__)


class MongoService:
    ONYXDB_SYSTEM_COLLECTION = "onyxdb_system"

    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._admin_db = self._mongo_client["admin"]

    async def create_database(self, name: str):
        db = self._mongo_client[name]
        collection = db[self.ONYXDB_SYSTEM_COLLECTION]
        collection.insert_one({})

    async def delete_database(self, name: str):
        self._mongo_client.drop_database(name)

    async def create_user(self, rq: CreateMongoUserRequestDTO):
        secret = client.CoreV1Api().read_namespaced_secret(rq.password_secret_name, rq.password_secret_namespace).data
        password = base64.b64decode(secret["password"]).decode("utf-8")

        roles = []
        for permission in rq.permissions:
            for role in permission.roles:
                roles.append({"db": permission.database, "role": role})

        self._admin_db.command(
            "createUser",
            rq.username,
            pwd=password,
            roles=roles
        )

    async def delete_user(self, rq: DeleteMongoUserRequestDTO):
        self._admin_db.command("dropUser", rq.username)
