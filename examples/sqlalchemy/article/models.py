from datetime import datetime

from fake import xor_transform
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Base",
    "User",
)


Base = declarative_base()


# Association table for the many-to-many relationship
user_group_association = Table(
    "user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)


class Group(Base):
    """Group model."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    def __repr__(self):
        return f"<Group(group='{self.name}')>"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Many-to-many relationship
    groups = relationship(
        "Group", secondary=user_group_association, backref="users"
    )

    # One-to-many relationship
    articles = relationship("Article", back_populates="author")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

    def set_password(self, password: str) -> None:
        self.password = xor_transform(password)


class Article(Base):
    """Article model."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True)
    content = Column(Text)
    headline = Column(Text)
    category = Column(String(255))
    pages = Column(Integer)
    auto_minutes_to_read = Column(Integer)
    image = Column(Text, nullable=True)
    pub_date = Column(DateTime, default=datetime.utcnow)
    safe_for_work = Column(Boolean, default=False)
    minutes_to_read = Column(Integer, default=5)
    author_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(JSON, default=list)

    # Relationships
    author = relationship("User", back_populates="articles")

    def __repr__(self):
        return (
            f"<Article(title='{self.title}', author='{self.author.username}')>"
        )
