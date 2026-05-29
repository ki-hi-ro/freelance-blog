from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import Work, WorkResponse
from app.database import SessionLocal

router = APIRouter()


def convert_work(work):
    return {
        "id": work.id,
        "title": work.title,
        "description": work.description,
        "github_url": work.github_url,
        "app_url": work.app_url,
        "technologies": work.technologies.split(",") if work.technologies else [],
        "created_at": work.created_at,
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/works", response_model=list[WorkResponse])
def read_works(db: Session = Depends(get_db)):
    works = db.query(models.Work).all()

    return [
        convert_work(work)
        for work in works
    ]


@router.post("/works", response_model=WorkResponse)
def create_work(
    work: Work,
    db: Session = Depends(get_db)
):
    new_work = models.Work(
        title=work.title,
        description=work.description,
        github_url=work.github_url,
        app_url=work.app_url,
        technologies=",".join(work.technologies),
    )

    db.add(new_work)
    db.commit()
    db.refresh(new_work)

    return convert_work(new_work)