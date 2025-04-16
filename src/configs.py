from typing import Type, Tuple
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, EnvSettingsSource, \
    YamlConfigSettingsSource


class HttpConfig(BaseModel):
    host: str = Field(default=...)
    port: int = Field(default=...)


class MongoConfig(BaseModel):
    uri: str = Field(default=...)
    cluster_id: UUID = Field(default=...)


class MdbConfig(BaseModel):
    base_url: str = Field(default=...)


class AgentConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def settings_customise_sources(
            cls, settings_cls: Type[BaseSettings], **kwargs
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(
                settings_cls,
                env_prefix="ONYXDB_",
                env_nested_delimiter="__",
                case_sensitive=False
            ),
            YamlConfigSettingsSource(settings_cls, yaml_file="./config.yml"),
        )

    http: HttpConfig = Field(default=...)
    mongo: MongoConfig = Field(default=...)
    mdb: MdbConfig = Field(default=...)
