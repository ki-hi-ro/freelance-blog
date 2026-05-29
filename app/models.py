from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    tags = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    work_time_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    github_url = Column(String)
    app_url = Column(String)
    technologies = Column(String)
    created_at = Column(DateTime, default=datetime.now)