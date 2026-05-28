from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import Post, PostResponse
from app.database import SessionLocal
from app import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/posts", response_model=list[PostResponse])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/posts", response_model=PostResponse)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        tags=",".join(post.tags),
        work_time_minutes=post.work_time_minutes,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post created successfully",
        "post": new_post,
    }


@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if db_post is None:
      raise HTTPException(status_code=404, detail="Post not found")

    db_post.title = post.title
    db_post.content = post.content
    db_post.tags = ",".join(post.tags)
    db_post.work_time_minutes = post.work_time_minutes

    db.commit()
    db.refresh(db_post)

    return {
        "message": "Post updated successfully",
        "post": db_post,
    }


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if db_post is None:
      raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()

    return {
        "message": "Post deleted successfully",
    }