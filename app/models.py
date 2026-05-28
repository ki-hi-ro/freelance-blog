from sqlalchemy import Column, Integer, String
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    tags = Column(String)
    work_time_minutes = Column(Integer)