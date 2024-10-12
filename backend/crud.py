from sqlalchemy.orm import Session
from sqlalchemy import desc
import backend.models as models
import backend.schemas as schemas
from backend.database import SessionLocal
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime, timedelta


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User
def get_user_by_tg_user_id(db: Session, tg_user_id: int):
    return db.query(models.User).filter(models.User.tg_user_id == tg_user_id).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(tg_user_id=user.tg_user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Post
def get_posts_by_tg_user_id(db: Session, tg_user_id: int):
    return db.query(models.Post).filter(models.Post.tg_user_id == tg_user_id).order_by(desc(models.Post.created_at))


def get_post_by_tg_msg_channel_id(db: Session, tg_msg_channel_id: int):
    return db.query(models.Post).filter(models.Post.tg_msg_channel_id == tg_msg_channel_id).first()


def get_post_by_tg_msg_group_id(db: Session, tg_msg_group_id: int):
    return db.query(models.Post).filter(models.Post.tg_msg_group_id == tg_msg_group_id).first()


def get_last_posts(db: Session, tg_user_id: int):
    one_week_ago = datetime.now() - timedelta(days=7)
    return db.query(models.Post).filter(models.Post.tg_user_id == tg_user_id, models.Post.created_at >= one_week_ago).all()


def create_post(db: Session, user: models.User, tg_msg_channel_id: int, feeling_category: str, feeling: str, text: str):
    post = models.Post(tg_user_id=user.tg_user_id, tg_msg_channel_id=tg_msg_channel_id, feeling_category=feeling_category, feeling=feeling, text=text)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, tg_msg_channel_id: int):
    delete = db.query(models.Post).filter(models.Post.tg_msg_channel_id == tg_msg_channel_id).delete()
    db.commit()
    return delete


def update_post(db: Session, tg_msg_channel_id: int, tg_msg_group_id: int):
    post = db.query(models.Post).filter(models.Post.tg_msg_channel_id == tg_msg_channel_id).first()
    post.tg_msg_group_id = tg_msg_group_id
    db.commit()
    return post


def update_post_report(db: Session, tg_msg_group_id: int, tg_user_id: int):
    post = db.query(models.Post).filter(models.Post.tg_msg_group_id == tg_msg_group_id).first()
    post.report_count += 1
    post.reported_by.append(tg_user_id)
    flag_modified(post, "reported_by")
    db.commit()
    return post


def update_post_like_count(db: Session, tg_msg_channel_id: int, like_count: int):
    post = db.query(models.Post).filter(models.Post.tg_msg_channel_id == tg_msg_channel_id).first()
    post.like_count = like_count
    db.commit()
    return post


# Answer
def get_answers_by_tg_user_id(db: Session, tg_user_id: int):
    return db.query(models.Answer).filter(models.Answer.tg_user_id == tg_user_id).order_by(desc(models.Answer.created_at))


def get_answer_by_tg_msg_ans_id(db: Session, tg_msg_ans_id: int):
    return db.query(models.Answer).filter(models.Answer.tg_msg_ans_id == tg_msg_ans_id).first()


def create_answer(db: Session, user: models.User, post: models.Post, answer: schemas.Answer):
    db_answer = models.Answer(
        tg_user_id=user.tg_user_id,
        tg_msg_group_id=post.tg_msg_group_id,
        tg_msg_ans_id=answer.tg_msg_ans_id,
        msg_group_text=answer.msg_group_text,
        msg_ans_text=answer.msg_ans_text,
    )
    db.add(db_answer)
    post.answer_count += 1
    db.commit()
    db.refresh(db_answer)

    return db_answer


def delete_answer(db: Session, tg_msg_ans_id: int, tg_msg_group_id: int):
    delete = db.query(models.Answer).filter(models.Answer.tg_msg_ans_id == tg_msg_ans_id).delete()
    post = db.query(models.Post).filter(models.Post.tg_msg_group_id == tg_msg_group_id).first()
    post.answer_count -= 1
    db.commit()
    return delete