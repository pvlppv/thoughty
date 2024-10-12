from typing import List
from backend.crud import get_db
import backend.schemas as schemas
import backend.crud as crud
import backend.models as models
from backend.database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

post_router = APIRouter(
    prefix="",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@post_router.get("/post/get_posts_by_tg_user_id/{tg_user_id}", response_model=List[schemas.Post])
def get_posts_by_tg_user_id(tg_user_id: int, db: Session = Depends(get_db)):
    return crud.get_posts_by_tg_user_id(db, tg_user_id)


@post_router.get("/post/get_post_by_tg_msg_channel_id/{tg_msg_channel_id}", response_model=schemas.Post)
def get_post_by_tg_msg_channel_id(tg_msg_channel_id: int, db: Session = Depends(get_db)):
    return crud.get_post_by_tg_msg_channel_id(db, tg_msg_channel_id)


@post_router.get("/post/get_post_by_tg_msg_group_id/{tg_msg_group_id}", response_model=schemas.Post)
def get_post_by_tg_msg_group_id(tg_msg_group_id: int, db: Session = Depends(get_db)):
    return crud.get_post_by_tg_msg_group_id(db, tg_msg_group_id)


@post_router.get("/post/get_last_posts/{tg_user_id}", response_model=List[schemas.Post])
def get_last_posts(tg_user_id: int, db: Session = Depends(get_db)):
    return crud.get_last_posts(db, tg_user_id)

@post_router.get("/post/get_amount")
def get_posts(db: Session = Depends(get_db)):
    return {"amount": db.query(models.Post).count()}


@post_router.post("/post/create/", response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    tg_user_id = crud.get_user_by_tg_user_id(db, tg_user_id=post.tg_user_id)
    if tg_user_id is None:
        raise HTTPException(status_code=400, detail="User is not registered")
    return crud.create_post(db=db, user=tg_user_id, tg_msg_channel_id=post.tg_msg_channel_id, feeling_category=post.feeling_category, feeling=post.feeling, text=post.text)


@post_router.delete("/post/delete/{tg_msg_channel_id}")
def delete_post(tg_msg_channel_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, tg_msg_channel_id)


@post_router.put("/post/update/{tg_msg_channel_id}/{tg_msg_group_id}")
def update_post(tg_msg_channel_id: int, tg_msg_group_id: int, db: Session = Depends(get_db)):
    return crud.update_post(db, tg_msg_channel_id, tg_msg_group_id)


@post_router.put("/post/update_like_count/{tg_msg_channel_id}/{like_count}")
def update_post_like_count(tg_msg_channel_id: int, like_count: int, db: Session = Depends(get_db)):
    return crud.update_post_like_count(db, tg_msg_channel_id, like_count)


@post_router.put("/post/update_report/{tg_msg_group_id}/{tg_user_id}", response_model=schemas.Post)
def update_post_report(tg_msg_group_id: int, tg_user_id: int, db: Session = Depends(get_db)):
    post = crud.get_post_by_tg_msg_group_id(db, tg_msg_group_id)
    if tg_user_id in post.reported_by:
        raise HTTPException(status_code=400, detail="User is already reported")
    return crud.update_post_report(db, tg_msg_group_id, tg_user_id)