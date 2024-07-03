from sqlalchemy.orm import Session
from app.schemas import PostCreate
from app.models import Post

def create_post(
    db: Session,
    request: PostCreate
):
    post = Post(**request.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post
