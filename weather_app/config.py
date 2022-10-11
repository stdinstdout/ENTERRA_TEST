from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "80a4796ed267b015ea14d7cecf5dde57"
    STORE_CACHE_TIME: int = 3600
    LOCAL_REDIS_URL: str = 'redis://redis'
