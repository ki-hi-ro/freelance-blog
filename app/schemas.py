from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    tags: list[str]
    start_time: datetime
    end_time: datetime


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True

class Work(BaseModel):
    title: str
    description: str
    github_url: str | None = None
    app_url: str | None = None
    technologies: list[str]


class WorkResponse(BaseModel):
    id: int
    title: str
    description: str
    github_url: str | None = None
    app_url: str | None = None
    technologies: list[str]
    created_at: datetime

    class Config:
        from_attributes = True