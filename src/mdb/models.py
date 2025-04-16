import uuid
from enum import StrEnum
from typing import List

from pydantic import BaseModel


class MongoHostType(StrEnum):
    mongod = "mongod"


class MongoHostStatus(StrEnum):
    unknown = "unknown"
    alive = "alive"
    dead = "dead"


class MongoHostRole(StrEnum):
    unknown = "unknown"
    primary = "primary"
    secondary = "secondary"


class MongoHost(BaseModel):
    name: str
    clusterId: uuid.UUID
    type: MongoHostType
    status: MongoHostStatus
    role: MongoHostRole


class UpdateMongoHostsRequest(BaseModel):
    hosts: List[MongoHost]
