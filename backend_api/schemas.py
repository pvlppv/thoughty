from pydantic import BaseModel
from datetime import datetime, timezone


class User(BaseModel):
    telegram_id: int


class Post(BaseModel):
    telegram_user_id: int
    telegram_message_id: int
    mood: str
    text: str
    created_at: datetime = datetime.now(timezone.utc)
