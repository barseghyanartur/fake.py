from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Set

from fake import xor_transform

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Group",
    "User",
)


@dataclass(frozen=True)
class Group:
    id: int
    name: str


@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    date_joined: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    password: Optional[str] = None
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    groups: Set[Group] = field(default_factory=set)

    def __str__(self):
        return self.username

    def set_password(self, password: str) -> None:
        self.password = xor_transform(password)


@dataclass
class Article:
    id: int
    title: str
    slug: str
    content: str
    headline: str
    category: str
    pages: int
    auto_minutes_to_read: int
    author: User
    image: Optional[str] = None  # Use str to represent the image path or URL
    pub_date: date = field(default_factory=date.today)
    safe_for_work: bool = False
    minutes_to_read: int = 5
    tags: List[str] = field(default_factory=list)

    def __str__(self):
        return self.title
