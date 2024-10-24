from backend.crud import get_db
import backend.schemas as schemas
import backend.crud as crud
import backend.models as models
from backend.database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

user_router = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/user/get_amount")
def get_users(db: Session = Depends(get_db)):
    return {"amount": db.query(models.User).count()}


@user_router.get("/user/{tg_user_id}", response_model=schemas.User)
def get_user(tg_user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_user_id(db, tg_user_id=tg_user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/user/create/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_user_id(db, tg_user_id=user.tg_user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)
