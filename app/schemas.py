from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: str
    work_time_minutes: int

    class Config:
        from_attributes = True