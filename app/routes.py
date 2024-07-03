from fastapi import APIRouter, Depends
from app import crud
from app.models import get_db
from sqlalchemy.orm import Session
from app.schemas import PostCreate

router = APIRouter()


@router.get("")
async def get_posts(db: Session = Depends(get_db)):
    pass

@router.post("/create", status_code=201)
async def create_post(request: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, request)