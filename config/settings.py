import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import SecretStr

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID")
    YANDEX_CLIENT_SECRET: SecretStr = os.getenv("YANDEX_CLIENT_SECRET")
    ADMINS: int = os.getenv("ADMINS")
    DB_URL: str = os.getenv("DB_URL")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")
    BOT_NAME: str = os.getenv("BOT_NAME")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()