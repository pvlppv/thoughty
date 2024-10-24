from typing import List
from backend.crud import get_db
import backend.schemas as schemas
import backend.crud as crud
import backend.models as models
from backend.database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

answer_router = APIRouter(
    prefix="",
    tags=["answer"],
    responses={404: {"description": "Not found"}},
)


@answer_router.get("/answer/get_answers_by_tg_user_id/{tg_user_id}", response_model=List[schemas.Answer])
def get_answers_by_tg_user_id(tg_user_id: int, db: Session = Depends(get_db)):
    return crud.get_answers_by_tg_user_id(db, tg_user_id)


@answer_router.get("/answer/get_answer_by_tg_msg_ans_id/{tg_msg_ans_id}", response_model=schemas.Answer)
def get_answer_by_tg_msg_ans_id(tg_msg_ans_id: int, db: Session = Depends(get_db)):
    return crud.get_answer_by_tg_msg_ans_id(db, tg_msg_ans_id)


@answer_router.post("/answer/create/", response_model=schemas.Answer)
def create_answer(answer: schemas.Answer, db: Session = Depends(get_db)):
    tg_user_id = crud.get_user_by_tg_user_id(db, tg_user_id=answer.tg_user_id)
    if tg_user_id is None:
        raise HTTPException(status_code=400, detail="User is not registered")
    tg_msg_group_id = crud.get_post_by_tg_msg_group_id(db, tg_msg_group_id=answer.tg_msg_group_id)
    if tg_msg_group_id is None:
        raise HTTPException(status_code=400, detail="Post is not created")
    return crud.create_answer(db=db, user=tg_user_id, post=tg_msg_group_id, answer=answer)


@answer_router.delete("/answer/delete/{tg_msg_ans_id}/{tg_msg_group_id}")
def delete_answer(tg_msg_ans_id: int, tg_msg_group_id: int, db: Session = Depends(get_db)):
    return crud.delete_answer(db, tg_msg_ans_id, tg_msg_group_id)