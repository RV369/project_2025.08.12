import os
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOGIN: ClassVar[str] = os.getenv('LOGIN')
    PASSWORD: ClassVar[str] = os.getenv('PASSWORD')

    class Config:
        env_file = '.env'


settings = Settings()
