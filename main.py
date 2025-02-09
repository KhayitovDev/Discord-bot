import asyncio
from app.kafka import KafkaService
from core.lifespan import startup, shutdown
from core.logger import logger
from core.config import settings
from app.bot import bot


async def main():
    """Start both the bot and MongoDB connection."""
    await startup()
    
    kafka_service = KafkaService(
        topic=settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER,
        group_id=settings.GROUP_ID
    )
    
    # Initialize Kafka consumer and producer
    await kafka_service.init_consumer()
    await kafka_service.init_producer()
    

    try:
       
        #Use asyncio.gather to run both the producer and consumer concurrently
        await asyncio.gather(
            # fetch_and_process_wiki_changes(kafka_service=kafka_service),  # Producer task
            # kafka_service.message_consumer(),  # Consumer task
            bot.start(settings.DISCORD_TOKEN)
        )
        
    except Exception as e:
        logger.error(f"Error while running program: {e}")
        
    finally:
        # Gracefully shutdown consumer and producer
        await kafka_service.shutdown_consumer()
        await kafka_service.shutdown_producer()


if __name__ == "__main__":
    asyncio.run(main())
