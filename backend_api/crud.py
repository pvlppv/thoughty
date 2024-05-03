from sqlalchemy.orm import Session
from sqlalchemy import desc
import backend_api.models as models
import backend_api.schemas as schemas
from backend_api.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_tg_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(telegram_id=user.telegram_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_posts_by_tg_user_id(db: Session, telegram_user_id: int):
    return db.query(models.Post).filter(models.Post.telegram_user_id == telegram_user_id).order_by(desc(models.Post.created_at))


def create_post(db: Session, user: models.User, telegram_message_id: int, mood: str, text: str):
    post = models.Post(telegram_user_id=user.telegram_id, telegram_message_id = telegram_message_id, mood=mood, text=text)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def delete_post(db: Session, telegram_message_id: int):
    delete = db.query(models.Post).filter(models.Post.telegram_message_id == telegram_message_id).delete()
    db.commit()
    return delete

