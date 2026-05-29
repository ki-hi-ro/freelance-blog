from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.routers import posts as posts_router
from app.database import engine, SessionLocal
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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