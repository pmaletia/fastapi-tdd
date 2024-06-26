from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.models import get_db
from app.schemas import PostCreateUpdate

router = APIRouter()


@router.post("", status_code=201)
async def create_post(request: PostCreateUpdate, db: Session = Depends(get_db)):
    return crud.create_post(db, request)


@router.put("/{post_id}")
async def update_post(
    post_id: int, request: PostCreateUpdate, db: Session = Depends(get_db)
):
    return crud.update_post(db, post_id, request)
