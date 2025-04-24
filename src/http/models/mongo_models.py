from pydantic import BaseModel


class CreateMongoDatabaseRequestDTO(BaseModel):
    name: str


class DeleteMongoDatabaseRequestDTO(BaseModel):
    name: str
