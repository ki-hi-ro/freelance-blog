from fastapi import FastAPI
from app.routers import posts

app = FastAPI()

app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"message": "Hello, my freelance blog"}