import os
from pydantic import MongoDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    
    MONGO_HOST: str = os.getenv('MONGO_HOST')
    MONGO_PORT: int = os.getenv('MONGO_PORT')
    MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME')
    MONGO_MIN_POOL_SIZE: int = os.getenv('MONGO_MIN_POOL_SIZE')
    MONGO_MAX_POOL_SIZE: int = os.getenv('MONGO_MAX_POOL_SIZE')
    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD')
    
    @property
    def mongo_dsn(self) -> MongoDsn:
        return MongoDsn(f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}")
    
    
    KAFKA_BROKER: str = os.getenv('KAFKA_BROKER')
    KAFKA_TOPIC: str = os.getenv('KAFKA_TOPIC')
    GROUP_ID: str = os.getenv('GROUP_ID')
    WIKI_STREAM_URL: str = os.getenv('WIKI_STREAM_URL')
    
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID: int = os.getenv('CHANNEL_ID')
    
    class Config:
        env_file = '.env'
    
settings = Settings()