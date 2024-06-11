from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "User",
)


@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    last_login: Optional[datetime]
    date_joined: Optional[datetime]
    password: Optional[str] = None
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True

    def __str__(self):
        return self.username


@dataclass
class Article:
    id: int
    title: str
    slug: str
    content: str
    headline: str
    category: str
    author: User
    image: Optional[str] = None  # Use str to represent the image path or URL
    pub_date: date = date.today()
    safe_for_work: bool = False
    minutes_to_read: int = 5

    def __str__(self):
        return self.title
