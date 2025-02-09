from beanie import Document
from typing import Optional, Any
import datetime

class WikipediaChanges(Document):
    title: str 
    title_url: str 
    comment: str 
    timestamp: Optional[Any] = None 
    user: str 
    wiki: str
    language: str
    date: Optional[Any] = None
    
    class Settings:
        name = "wikipedia"
        
    def set_date_from_timestamp(self):
        if self.timestamp:
            self.date = self.timestamp.date()
        
class LanguagePreference(Document):
    user_id: int 
    language: str 
    
    class Settings:
        name = "language_preference"