from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Post(BaseModel):
    title: str
    content: str
    tags: list[str]
    work_time_minutes: int


posts = [
    {
        "id": 1,
        "title": "職人的フリーランスへの第一歩",
        "content": "FastAPIで自分のブログサービスを作り始めた。",
        "tags": ["FastAPI", "Python", "Freelance"],
        "work_time_minutes": 30,
    },
    {
        "id": 2,
        "title": "理想の働き方につながるものだけを積む",
        "content": "市場に見える形で成果物を積み上げていく。",
        "tags": ["Career", "Portfolio"],
        "work_time_minutes": 45,
    },
]


@router.get("/posts")
def read_posts():
    return posts


@router.get("/posts/{post_id}")
def read_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post

    return {"error": "Post not found"}


@router.post("/posts")
def create_post(post: Post):
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "work_time_minutes": post.work_time_minutes,
    }

    posts.append(new_post)

    return {
        "message": "Post created successfully",
        "post": new_post,
    }