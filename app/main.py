from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.routers import posts as posts_router
from app.routers import works as works_router

from app.database import engine, SessionLocal
from app import models

import markdown

from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts_router.router)
app.include_router(works_router.router)

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

@app.post("/posts-page")
def create_post_from_page(
    title: str = Form(...),
    content: str = Form(...),
    task_type: str = Form(""),
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

    new_post = models.Post(
        title=title,
        content=content,
        task_type=task_type,
        start_time=start_dt,
        end_time=end_dt,
        work_time_minutes=work_time_minutes,
        work_id=work_id,
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
    task_type: str = Form(""),  
    work_time_minutes: int = Form(...),
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        post.title = title
        post.content = content
        post.task_type = task_type
        post.work_time_minutes = work_time_minutes
        db.commit()

    return RedirectResponse(url="/posts-page", status_code=303)

@app.get("/posts-page/{post_id}")
def post_detail_page(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        post.content = markdown.markdown(
            post.content,
            extensions=["fenced_code"]
        )

    return templates.TemplateResponse(
        request,
        "post_detail.html",
        {"post": post}
    )

@app.get("/works-page")
def works_page(request: Request, db: Session = Depends(get_db)):
    works = db.query(models.Work).all()

    for work in works:
        work.description = markdown.markdown(work.description)

    return templates.TemplateResponse(
        request,
        "works.html",
        {"works": works}
    )

@app.post("/works-page")
def create_work_from_page(
    title: str = Form(...),
    description: str = Form(...),
    github_url: str = Form(""),
    app_url: str = Form(""),
    technologies: str = Form(""),
    db: Session = Depends(get_db),
):
    new_work = models.Work(
        title=title,
        description=description,
        github_url=github_url,
        app_url=app_url,
        technologies=technologies,
    )

    db.add(new_work)
    db.commit()

    return RedirectResponse(url="/works-page", status_code=303)

@app.get("/works-page/{work_id}")
def work_detail_page(
    work_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    work = (
        db.query(models.Work)
        .filter(models.Work.id == work_id)
        .first()
    )

    return templates.TemplateResponse(
        request,
        "work_detail.html",
        {"work": work}
    )