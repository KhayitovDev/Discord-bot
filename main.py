import asyncio
from core.lifespan import startup, shutdown

async def main():
    """Start both the bot and MongoDB connection."""
    await startup() 
    #await shutdown()
   
# Execute bot
if __name__ == "__main__":
    asyncio.run(main())