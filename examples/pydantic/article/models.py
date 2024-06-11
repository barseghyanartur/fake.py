from datetime import date, datetime
from typing import List, Optional, Set

from fake import xor_transform
from pydantic import BaseModel, Field

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Group",
    "User",
)


class Group(BaseModel):
    id: int
    name: str

    class Config:
        allow_mutation = False

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        if isinstance(other, Group):
            return self.id == other.id and self.name == other.name
        return False


class User(BaseModel):
    id: int
    username: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    date_joined: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    password: Optional[str] = Field("", max_length=255)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=True)
    groups: Set[Group] = Field(default_factory=set)

    class Config:
        extra = "allow"  # For testing purposes only

    def __str__(self):
        return self.username

    def set_password(self, password: str) -> None:
        self.password = xor_transform(password)


class Article(BaseModel):
    id: int
    title: str = Field(max_length=255)
    slug: str = Field(max_length=255, unique=True)
    content: str
    headline: str
    category: str = Field(max_length=255)
    pages: int
    auto_minutes_to_read: int
    author: User
    image: Optional[str] = None  # Use str to represent the image path or URL
    pub_date: date = Field(default_factory=date.today)
    safe_for_work: bool = False
    minutes_to_read: int = 5
    tags: List[str] = Field(default_factory=list)

    class Config:
        extra = "allow"  # For testing purposes only

    def __str__(self):
        return self.title
