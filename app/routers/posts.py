from fastapi import APIRouter
from pydantic import BaseModel

# APIRouterインスタンスを作成 
# posts関連APIをまとめるための「小さなアプリ」のような存在
router = APIRouter()

# 投稿データの型定義 
# POST /posts のリクエスト時に使われる
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

# 記事一覧取得API
# GET /posts
@router.get("/posts")
def read_posts():
    # postsリストをそのまま返す
    return posts

# 記事詳細取得API 
# GET /posts/1 のように使う
@router.get("/posts/{post_id}")
def read_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post

    return {"error": "Post not found"}

# 記事作成API 
# POST /posts
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