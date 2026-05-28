from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, my freelance blog"}


@app.get("/posts")
def read_posts():
    return [
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