from datetime import timedelta

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DEBUG: bool = Field(env="FLASK_DEBUG", default=False)
    SECRET_KEY: str = Field(env="SECRET_KEY")

    pg_db_name: str = Field(env="POSTGRES_DB")
    pg_db_user: str = Field(env="POSTGRES_USER")
    pg_db_password: str = Field(env="POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="POSTGRES_DB_HOST")
    pg_db_port: str = Field(env="POSTGRES_DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://localhost:6390"
    JWT_SECRET_KEY: str = Field(env="SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return (
            f"postgresql+psycopg2://{self.pg_db_user}:{self.pg_db_password}"
            f"@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
        )


config = Settings()
