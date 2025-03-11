from typing import Optional, List
from pydantic import BaseModel

class Message(BaseModel):
    type: str
    id: str
    text: Optional[str] = None
    mention: Optional[dict] = None

class Events(BaseModel):
    message: Message
    replyToken: str
    source: dict

class WebhookBody(BaseModel):
    events: List[Events]