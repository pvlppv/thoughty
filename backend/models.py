from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, TIMESTAMP, ARRAY
from backend.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(BigInteger, index=True, unique=True)
    role = Column(String, index=True, default="user")
    joined_at = Column(TIMESTAMP(timezone=True), default=func.now())


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(BigInteger, ForeignKey("users.tg_user_id", ondelete="CASCADE"), index=True)
    tg_msg_channel_id = Column(BigInteger, index=True, unique=True)
    tg_msg_group_id = Column(BigInteger, index=True, default=0, unique=True)
    feeling_category = Column(String, index=True)
    feeling = Column(String, index=True)
    text = Column(String, index=True)
    like_count = Column(Integer, index=True, default=0)
    answer_count = Column(Integer, index=True, default=0)
    report_count = Column(Integer, index=True, default=0)
    reported_by = Column(ARRAY(BigInteger), index=True, default=[])
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())

    tg_user_id_ref = relationship("User", cascade="all, delete", foreign_keys=[tg_user_id])


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(BigInteger, ForeignKey("users.tg_user_id", ondelete="CASCADE"), index=True)
    tg_msg_group_id = Column(BigInteger, ForeignKey("posts.tg_msg_group_id", ondelete="CASCADE"), index=True)
    tg_msg_ans_id = Column(BigInteger, index=True, unique=True)
    msg_group_text = Column(String, index=True)
    msg_ans_text = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())

    tg_user_id_ref = relationship("User", cascade="all, delete", foreign_keys=[tg_user_id])
    tg_msg_group_id_ref = relationship("Post", cascade="all, delete", foreign_keys=[tg_msg_group_id])
