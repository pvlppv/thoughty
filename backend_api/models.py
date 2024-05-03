from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, TIMESTAMP
from backend_api.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, index=True, unique=True)
    joined_at = Column(TIMESTAMP(timezone=True), default=func.now())


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(BigInteger, ForeignKey("users.telegram_id"), index=True)
    telegram_message_id = Column(BigInteger, index=True)
    mood = Column(String, index=True)
    text = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
