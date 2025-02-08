from beanie import Document

class WikipediaChanges(Document):
    page_title: str 
    url: str 
    content: str 
    language: str 
    
    
    class Settings:
        name = "wikipedia"