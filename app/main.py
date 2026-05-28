from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.routers import posts as posts_router
from app.database import engine, SessionLocal
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts_router.router)

templates = Jinja2Templates(directory="app/templates")

sample_posts = [
    {"title": "記事1", "content": "本文1"},
    {"title": "記事2", "content": "本文2"},
]


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
def posts_page(request: Request):
  return templates.TemplateResponse(
      request,
      "posts.html",
      {"posts": sample_posts}
  )