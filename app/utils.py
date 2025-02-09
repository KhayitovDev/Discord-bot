import re
from datetime import datetime, timezone
from app.models import WikipediaChanges, LanguagePreference
from core.logger import logger


async def convert_timestamp(timestamp):
    """Convert timestamp from Unix to human-readable format."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


async def clean_message(event):
    try:
        def clean_comment(comment: str) -> str:
            comment = re.sub(r'\[\[.*?\|', '', comment)  
            comment = re.sub(r'\[\[.*?\]\]', '', comment)  
            comment = re.sub(r'[^\x00-\x7F]+', '', comment)  
            return comment

        cleaned_event = {
            'title': event.get('title', ''),
            'title_url': event.get('title_url', ''),
            'comment': clean_comment(event.get('comment', '')),
            'timestamp': event.get('timestamp', 0),
            'user': event.get('user', 'Unknown'),
            'wiki': event.get('wiki', 'Unknown'),
        }
        if cleaned_event['timestamp']:
            cleaned_event['timestamp'] = await convert_timestamp(cleaned_event['timestamp'])

        return cleaned_event

    except Exception as e:
        logger.error(f"Error while cleaning the event: {e}")
        return {}


async def insert_event(event, lan: str):

    cleaned_event = await clean_message(event=event)
    data = WikipediaChanges(
        title = cleaned_event.get('title', ''),
        title_url = cleaned_event.get('title_url', ''),
        comment = cleaned_event.get('comment', ''),
        timestamp = cleaned_event.get('timestamp', 0),
        user = cleaned_event.get('user', 'Unknown'),
        wiki = cleaned_event.get('wiki', 'Unknown'),   
        language=lan,
        date=datetime.now()
    )
    await data.insert()

async def insert_language_preference(user_id: int, language: str):
  
    set_language = LanguagePreference(
        user_id=user_id,
        language=language
    )
    await set_language.insert()