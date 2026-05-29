from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.routers import posts as posts_router
from app.database import engine, SessionLocal
from app import models

import markdown

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts_router.router)

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, my freelance blog"}


@app.get("/posts-page")
def posts_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    for post in posts:
        post.content = markdown.markdown(
            post.content,
            extensions=[
                "fenced_code",
                "codehilite",
            ]
        )

    return templates.TemplateResponse(
        request,
        "posts.html",
        {"posts": posts}
    )

@app.post("/posts-page")
def create_post_from_page(
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
    work_time_minutes: int = Form(...),
    db: Session = Depends(get_db),
):
    new_post = models.Post(
        title=title,
        content=content,
        tags=tags,
        work_time_minutes=work_time_minutes,
    )

    db.add(new_post)
    db.commit()

    return RedirectResponse(url="/posts-page", status_code=303)

@app.post("/posts-page/{post_id}/delete")
def delete_post_from_page(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if db_post:
        db.delete(db_post)
        db.commit()

    return RedirectResponse(url="/posts-page", status_code=303)

@app.get("/posts-page/{post_id}/edit")
def edit_post_page(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    return templates.TemplateResponse(
        request,
        "edit_post.html",
        {"post": post}
    )

@app.post("/posts-page/{post_id}/edit")
def update_post_from_page(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
    work_time_minutes: int = Form(...),
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        post.title = title
        post.content = content
        post.tags = tags
        post.work_time_minutes = work_time_minutes
        db.commit()

    return RedirectResponse(url="/posts-page", status_code=303)