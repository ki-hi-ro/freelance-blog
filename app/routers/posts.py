from app.schemas import Post, PostResponse
from app import models
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models
import markdown
from datetime import datetime
from fastapi.templating import Jinja2Templates
from app.database import get_db

router = APIRouter()

def convert_post(post):
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "task_type": post.task_type,
        "start_time": post.start_time,
        "end_time": post.end_time,
        "work_time_minutes": post.work_time_minutes,
        "created_at": post.created_at,
    }

templates = Jinja2Templates(directory="app/templates")


# =========================
# API Endpoints
# =========================

# Create
@router.post("/posts", response_model=PostResponse)
def create_post(post: Post, db: Session = Depends(get_db)):
    work_time_minutes = int((post.end_time - post.start_time).total_seconds() / 60)

    new_post = models.Post(
        title=post.title,
        content=post.content,
        task_type=post.task_type,
        work_time_minutes=work_time_minutes,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return convert_post(new_post)


# Read（一覧）
@router.get("/posts", response_model=list[PostResponse])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return [convert_post(post) for post in posts]


# Read（詳細）
@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return convert_post(post)    


# Update（処理）
@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if db_post is None:
      raise HTTPException(status_code=404, detail="Post not found")

    db_post.title = post.title
    db_post.content = post.content
    db_post.task_type = post.task_type
    db_post.work_time_minutes = post.work_time_minutes

    db.commit()
    db.refresh(db_post)

    return convert_post(db_post)


# Delete（処理）
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


# =========================
# HTML Pages
# =========================

# Create（画面）
@router.get("/posts-page/new")
def new_post_page(
    request: Request,
    work_id: int | None = None,
    db: Session = Depends(get_db)
):
    works = db.query(models.Work).all()

    return templates.TemplateResponse(
        request,
        "new_post.html",
        {
            "works": works,
            "selected_work_id": work_id
        }
    )


# Create（処理）
@router.post("/posts-page")
def create_post_from_page(
    content: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    work_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    work_time_minutes = int(
        (end_dt - start_dt).total_seconds() / 60
    )

    title = content.splitlines()[0].replace("#", "").strip() if content.strip() else "作業ログ"

    new_post = models.Post(
        title=title,
        content=content,
        task_type="",
        start_time=start_dt,
        end_time=end_dt,
        work_time_minutes=work_time_minutes,
        work_id=work_id,
    )

    db.add(new_post)
    db.commit()

    if work_id:
        return RedirectResponse(url=f"/works-page/{work_id}", status_code=303)

    return RedirectResponse(url="/posts-page", status_code=303)


# Read（一覧）
@router.get("/posts-page")
def posts_page(
    request: Request,
    work_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)

    if work_id:
        query = query.filter(
            models.Post.work_id == work_id
        )

    posts = query.all()

    works = db.query(models.Work).all()

    return templates.TemplateResponse(
        request,
        "posts.html",
        {"posts": posts, "works": works}
    )


# Read（詳細）
@router.get("/posts-page/{post_id}")
def post_detail_page(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    duration_minutes = int(
        (post.end_time - post.start_time).total_seconds() / 60
    )

    if post:
        post.content = markdown.markdown(
            post.content,
            extensions=["fenced_code"]
        )

    return templates.TemplateResponse(
        request,
        "post_detail.html",
        {
            "post": post,
            "duration_minutes": duration_minutes
        }
    )


# Update（画面）
@router.get("/posts-page/{post_id}/edit")
def edit_post_page(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    return templates.TemplateResponse(
        request,
        "edit_post.html",
        {"post": post}
    )


# Update（処理）
@router.post("/posts-page/{post_id}/edit")
def update_post_from_page(
    post_id: int,
    content: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    work_time_minutes = int(
        (end_dt - start_dt).total_seconds() / 60
    )

    title = content.splitlines()[0].replace("#", "").strip() if content.strip() else "作業ログ"

    if post:
        post.title = title
        post.content = content
        post.start_time = start_dt
        post.end_time = end_dt
        post.work_time_minutes = work_time_minutes
        db.commit()

        return RedirectResponse(
            url=f"/works-page/{post.work_id}",
            status_code=303
        )

    return RedirectResponse(url="/posts-page", status_code=303)


# Delete（処理）
@router.post("/posts-page/{post_id}/delete")
def delete_post_from_page(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if db_post:
        work_id = db_post.work_id
        db.delete(db_post)
        db.commit()

    return RedirectResponse(
        url=f"/works-page/{work_id}",
        status_code=303
    )