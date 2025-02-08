
import os 
from pydantic import MongoDsn
from pydantic_core import Url
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = 'Wiki'
    MONGO_MIN_POOL_SIZE: int = 2
    MONGO_MAX_POOL_SIZE: int = 4
    MONGO_USER: str = 'discord_wiki_user'
    MONGO_PASSWORD: str = ''
    
    @property
    def mongo_dsn(self) -> MongoDsn:
        return MongoDsn(f"mongodb://localhost:27017")
    
settings = Settings()