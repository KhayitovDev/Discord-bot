from connections.mongo import AsyncMongoConnection
from contextlib import asynccontextmanager

async def startup():
    await AsyncMongoConnection().connect()

async def shutdown():
    await AsyncMongoConnection().disconnect()
    

