from motor.motor_asyncio import AsyncIOMotorClient
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation

from pymongo.errors import ConnectionFailure
from beanie import init_beanie
from connections import Connection

from app.models import LanguagePreference, WikipediaChanges

from core.logger import logger
from core.config import settings

class AsyncMongoConnection(Connection):

    async def connect(self) -> AsyncIOMotorClient:
        try:
            motor_client = AsyncIOMotorClient(
                settings.mongo_dsn.unicode_string(),
                minPoolSize=settings.MONGO_MIN_POOL_SIZE,
                maxPoolSize=settings.MONGO_MAX_POOL_SIZE
            )
            codec_options = CodecOptions(uuid_representation=UuidRepresentation.STANDARD)
            await motor_client.admin.command('ping')
            db = motor_client.get_database(settings.MONGO_DB_NAME, codec_options=codec_options)
            await init_beanie(
                database=db,
                document_models=[WikipediaChanges, LanguagePreference], #we include beanie models here 
                multiprocessing_mode=True
            )
            logger.info("Connected to AsyncMongoConnection\n")
            setattr(self, "_client", motor_client)
        except ConnectionFailure as e:
            logger.exception(f"AsyncMongoConnection connection failed: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred while connecting to AsyncMongoConnection: {e}")