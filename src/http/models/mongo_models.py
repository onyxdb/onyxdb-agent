from typing import List

from pydantic import BaseModel


class CreateMongoDatabaseRequestDTO(BaseModel):
    name: str


class DeleteMongoDatabaseRequestDTO(BaseModel):
    name: str


class MongoPermissionDTO(BaseModel):
    database: str
    roles: List[str]


class CreateMongoUserRequestDTO(BaseModel):
    username: str
    password_secret_name: str
    password_secret_namespace: str
    permissions: List[MongoPermissionDTO]


class DeleteMongoUserRequestDTO(BaseModel):
    username: str
