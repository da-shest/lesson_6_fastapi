from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'ABOBA'
    default_page_size: int = 15
    max_page_size: int = 60
    default_offset: int = 0
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings() -> Settings:
    return Settings()
