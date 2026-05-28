from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True