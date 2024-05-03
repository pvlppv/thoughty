from typing import List
from backend_api.crud import get_db
import backend_api.schemas as schemas
import backend_api.crud as crud
import backend_api.models as models
from backend_api.database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

post_router = APIRouter(
    prefix="",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@post_router.get("/post/get/{telegram_user_id}", response_model=List[schemas.Post])
def get_posts_by_tg_user_id(telegram_user_id: int, db: Session = Depends(get_db)):
    return crud.get_posts_by_tg_user_id(db, telegram_user_id)


@post_router.get("/post/get_amount")
def get_posts(db: Session = Depends(get_db)):
    return {"amount": db.query(models.Post).count()}


@post_router.post("/post/create/", response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    telegram_user_id = crud.get_user_by_tg_id(db, telegram_id=post.telegram_user_id)
    if telegram_user_id is None:
        raise HTTPException(status_code=400, detail="User is not registered")
    return crud.create_post(db=db, user=telegram_user_id, telegram_message_id=post.telegram_message_id, mood=post.mood, text=post.text)


@post_router.delete("/post/delete/{telegram_message_id}")
def delete_post(telegram_message_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, telegram_message_id)