from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------
    app_name: str
    app_version: str
    api_prefix: str
    debug: bool

    # ---------------------------------------------------------
    # Server / Uvicorn
    # ---------------------------------------------------------
    app_host: str
    app_port: int
    app_reload: bool

    # ---------------------------------------------------------
    # MySQL
    # ---------------------------------------------------------
    mysql_driver: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_charset: str

    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------
    cors_origins: str

    # ---------------------------------------------------------
    # SQLAlchemy
    # ---------------------------------------------------------
    sql_echo: bool

    # ---------------------------------------------------------
    # TELEGRAM
    # ---------------------------------------------------------
    telegram_api: str
    telegram_webhook_secret: str
    telegram_webhook_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=self.mysql_driver,
            username=self.mysql_user,
            password=self.mysql_password,
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            query={
                "charset": self.mysql_charset,
            },
        )

    @property
    def cors_origin_list(self) -> list[str]:
        """
        Convert:
        CORS_ORIGINS=*
        to:
        ["*"]

        Or:
        CORS_ORIGINS=http://localhost:3000,http://localhost:5173
        to:
        [
            "http://localhost:3000",
            "http://localhost:5173",
        ]
        """
        if self.cors_origins.strip() == "*":
            return ["*"]

        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()