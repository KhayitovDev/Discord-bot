import aiohttp
import json
from core.logger import logger
from core.config import settings

from app.kafka import KafkaService



async def fetch_and_process_wiki_changes(kafka_service: KafkaService):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.WIKI_STREAM_URL) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch data from wiki: {response.status}")
                    
                async for line in response.content:
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data:'):
                            content = decoded_line[5:].strip()
                            try:
                                event = json.loads(content)
                                await kafka_service.publish_to_kafka(change_event=event)
                            except json.JSONDecodeError:
                                logger.error(f"Non-json message received: {decoded_line}")
                            except Exception as e:
                                logger.error(f"Error while processing line: {e}")                          
    except Exception as e:
        logger.error(f"Error with Wikipedia fetching: {e}")
        