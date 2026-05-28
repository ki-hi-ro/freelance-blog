from fastapi import FastAPI
from app.routers import posts
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"message": "Hello, my freelance blog"}