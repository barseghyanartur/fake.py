from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "User",
)


class User(BaseModel):
    id: int
    username: str = Field(..., max_length=255)
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    password: Optional[str] = Field("", max_length=255)
    last_login: Optional[datetime]
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=True)
    date_joined: Optional[datetime]

    class Config:
        extra = "allow"  # For testing purposes only

    def __str__(self):
        return self.username


class Article(BaseModel):
    id: int
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255, unique=True)
    content: str
    image: Optional[str] = None  # Use str to represent the image path or URL
    pub_date: date = Field(default_factory=date.today)
    safe_for_work: bool = False
    minutes_to_read: int = 5
    author: User

    class Config:
        extra = "allow"  # For testing purposes only

    def __str__(self):
        return self.title
