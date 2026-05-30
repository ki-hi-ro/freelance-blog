from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import posts as posts_router
from app.routers import works as works_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts_router.router)
app.include_router(works_router.router)