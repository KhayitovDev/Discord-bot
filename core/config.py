
from pydantic import MongoDsn
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
    
    
    KAFKA_BROKER: str = 'localhost:19092'
    KAFKA_TOPIC: str = 'wikipedia-recent-changes'
    GROUP_ID: str = 'discord-consumer-group'
    WIKI_STREAM_URL: str = "https://stream.wikimedia.org/v2/stream/recentchange"
    
    DISCORD_TOKEN: str
    CHANNEL_ID: int
    
settings = Settings()