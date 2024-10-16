from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.dev.env'),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8',
        extra='ignore')

    debug: bool = True
    url: str = 'http://127.0.0.1:8000'
    database_url: str = 'postgresql+psycopg2://postgres:1234@localhost:5432/database'
    redis_url: str = 'redis://localhost:6379/0'
    bot_token: str = '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base_webhook_url: str = 'https://my.host.name'
    webhook_path: str = '/path/to/webhook'
    telegram_my_token: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Additional security token for webhook
    channel_id: int
    group_id: int


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
