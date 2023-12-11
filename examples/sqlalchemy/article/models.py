from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Base",
    "User",
)


Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, nullable=True)

    articles = relationship("Article", back_populates="author")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Article(Base):
    """Article model."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True)
    content = Column(Text)
    image = Column(Text, nullable=True)
    pub_date = Column(DateTime, default=datetime.utcnow)
    safe_for_work = Column(Boolean, default=False)
    minutes_to_read = Column(Integer, default=5)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")

    def __repr__(self):
        return (
            f"<Article(title='{self.title}', author='{self.author.username}')>"
        )
