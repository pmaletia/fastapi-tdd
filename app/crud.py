from sqlalchemy.orm import Session

from app.models import Post
from app.schemas import PostCreate


def create_post(db: Session, request: PostCreate):
    post = Post(**request.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post_instance(db: Session, post_id: str):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if not post:
        raise Exception("Post not found")
    return post


def update_post(db: Session, post_id: str, request: PostCreate):
    post = get_post_instance(db, post_id)
    post.title = request.title
    post.description = request.description
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
