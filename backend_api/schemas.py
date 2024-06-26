from pydantic import BaseModel
from datetime import datetime, timezone


class User(BaseModel):
    tg_user_id: int
    role: str = "user"


class Post(BaseModel):
    tg_user_id: int
    tg_msg_channel_id: int
    tg_msg_group_id: int = 0
    feeling_category: str
    feeling: str
    text: str
    like_count: int = 0
    answer_count: int = 0
    report_count: int = 0
    reported_by: list = []
    created_at: datetime = datetime.now(timezone.utc)


class Answer(BaseModel):
    tg_user_id: int
    tg_msg_group_id: int
    tg_msg_ans_id: int
    msg_group_text: str
    msg_ans_text: str
    created_at: datetime = datetime.now(timezone.utc)