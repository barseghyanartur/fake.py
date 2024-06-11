from datetime import datetime
from typing import List, Optional

from fake import xor_transform
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Group",
    "User",
)


class UserGroup(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True,
    )
    group_id: Optional[int] = Field(
        default=None,
        foreign_key="group.id",
        primary_key=True,
    )


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})
    users: List["User"] = Relationship(
        back_populates="groups",
        link_model=UserGroup,
    )

    def __repr__(self):
        return f"<Group(group='{self.name}')>"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    first_name: str
    last_name: str
    email: str
    date_joined: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime]
    password: str
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=True)
    groups: List[Group] = Relationship(
        back_populates="users",
        link_model=UserGroup,
    )
    articles: List["Article"] = Relationship(back_populates="author")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

    def set_password(self, password: str) -> None:
        self.password = xor_transform(password)


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(sa_column_kwargs={"unique": True})
    content: str
    headline: str
    category: str
    pages: int
    auto_minutes_to_read: int
    image: Optional[str]
    pub_date: datetime = Field(default_factory=datetime.utcnow)
    safe_for_work: bool = Field(default=False)
    minutes_to_read: int = Field(default=5)
    author_id: int = Field(foreign_key="user.id")
    tags: Optional[List[str]] = Field(
        default_factory=list,
        sa_column=Column(JSON),
    )
    author: User = Relationship(back_populates="articles")

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return (
            f"<Article(title='{self.title}', author='{self.author.username}')>"
        )
