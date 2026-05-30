from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from app.routers import posts as posts_router
from app.routers import works as works_router
from app.database import engine
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts_router.router)
app.include_router(works_router.router)

templates = Jinja2Templates(directory="app/templates")


# Read
@app.get("/")
def top_page(
    request: Request,
    db: Session = Depends(get_db)
):
    works = (
        db.query(models.Work)
        .order_by(models.Work.id.desc())
        .limit(2)
        .all()
    )

    return templates.TemplateResponse(
        request,
        "top.html",
        {"works": works}
    )