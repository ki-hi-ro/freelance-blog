from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int