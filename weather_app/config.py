import os
from pydantic import BaseSettings, Field    


class Settings(BaseSettings):
    api_key: str = "80a4796ed267b015ea14d7cecf5dde57"
    LOCAL_REDIS_URL: str = 'redis://0.0.0.0:6379'