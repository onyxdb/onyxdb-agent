from pydantic import BaseModel


class CreateMongoDatabaseRequest(BaseModel):
    name: str


class DeleteMongoDatabaseRequest(BaseModel):
    name: str
