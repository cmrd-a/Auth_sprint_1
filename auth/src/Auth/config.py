from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    flask_debug: bool = Field(env="FLASK_DEBUG", default=False)
    secret_key: str = Field(env="SECRET_KEY")

    pg_db_name: str = Field(env="POSTGRES_DB")
    pg_db_user: str = Field(env="POSTGRES_USER")
    pg_db_password: str = Field(env="POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="POSTGRES_DB_HOST")
    pg_db_port: str = Field(env="POSTGRES_DB_PORT")

    @property
    def pg_url(self):
        return (
            f"postgresql+psycopg2://{self.pg_db_user}:{self.pg_db_password}"
            f"@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
        )


config = Settings()

DEBUG = config.flask_debug
SQLALCHEMY_DATABASE_URI = config.pg_url
SECRET_KEY = config.secret_key
SQLALCHEMY_TRACK_MODIFICATIONS = False
