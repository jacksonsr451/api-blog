from decouple import config

from .logger_config import configure_logging


class Settings:
    SERVER_HOST: str = config("SERVER_HOST", default="127.0.0.1", cast=str)
    SERVER_PORT: int = config("SERVER_PORT", default=8000, cast=int)
    SERVER_RELOAD: bool = config("SERVER_RELOAD", default=False, cast=bool)
    SERVER_WORKERS: int = config("SERVER_WORKERS", default=1, cast=int)
    APP_ENV: str = config("APP_ENV", default="production", cast=str)
    APP_NAME: str = config("APP_NAME", default="my_app", cast=str)
    API_KEY: str = config("API_KEY", default="your-api-key", cast=str)
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379", cast=str)
    KEYCLOAK_URL: str = config("KEYCLOAK_URL", default="keycloak-url", cast=str)
    KEYCLOAK_JWK_URI: str = config("KEYCLOAK_JWK_URI", default="keycloak-jwk", cast=str)
    POSTGRES_URL: str = config("POSTGRES_URL", default="sqlite:///./test.db", cast=str)

    def is_dev(self) -> bool:
        return self.APP_ENV == "development"

    def is_prod(self) -> bool:
        return self.APP_ENV == "production"

    def configure_logging(self):
        return configure_logging(self.is_dev(), config("APP_NAME"))


settings = Settings()
