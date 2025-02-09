from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from core.config import settings
from core.logger import logger
from app.utils import insert_event, clean_message
import json

class KafkaService:
    
    def __init__(self, topic, bootstrap_servers, group_id):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.producer = None

    async def init_consumer(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest'
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer for topic '{self.topic}' started.")

    async def shutdown_consumer(self):
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"Kafka consumer for topic '{self.topic}' stopped.")
        else:
            logger.warning("Kafka consumer is not initialized.")

    async def init_producer(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        await self.producer.start()
        logger.info("Kafka producer started.")

    async def shutdown_producer(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped.")
        else:
            logger.warning("Kafka producer is not initialized.")

    async def publish_to_kafka(self, change_event):
        try:
            key = str(change_event.get("meta", {}).get("id"))
            await self.producer.send_and_wait(
                self.topic, key=key.encode(), value=json.dumps(change_event).encode()
            )
            logger.info(f"Published to Kafka: {key}")
        except Exception as e:
            logger.error(f"Error while publishing to Kafka: {e}")
            
    async def message_consumer(self):
        """Consume messages from Kafka and process them."""
        try:
            async for message in self.consumer:
                raw_event = message.value.decode('utf-8')
                try:
                    event = json.loads(raw_event)
                    server_name = event.get('server_name', '')
                    language = server_name.split('.')[0] if server_name else 'unknown'
                
                    await insert_event(event=event, lan=language)

                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON message: {raw_event}")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")

