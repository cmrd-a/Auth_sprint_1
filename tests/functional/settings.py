from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    es_host: str = Field(env="ES_HOST", default="http://localhost")
    es_port: str = Field(env="ES_PORT", default=9200)

    redis_host: str = Field(env="REDIS_HOST", default="redis://localhost")
    redis_port: int = Field(env="REDIS_PORT", default=6379)

    service_host: str = Field(env="SERVICE_HOST", default="http://localhost")
    service_port: int = Field(env="SERVICE_PORT", default=8000)

    @property
    def es_url(self):
        return f"{self.es_host}:{self.es_port}"

    @property
    def redis_url(self):
        return f"{self.redis_host}:{self.redis_port}"

    @property
    def service_url(self):
        return f"{self.service_host}:{self.service_port}"


settings = Settings()
