from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str = Field(..., max_length=255)
    slug: str = Field(..., unique=True)
    content: str
    image: Optional[str] = None  # Use str to represent the image path or URL
    pub_date: datetime = Field(default_factory=datetime.now)
    safe_for_work: bool = False
    minutes_to_read: int = 5
    author_id: int  # Assuming author is represented by an integer ID

    class Config:
        orm_mode = True


# Example usage
# article = Article(
#     title="Sample Title",
#     slug="sample-title",
#     content="Sample content",
#     author_id=1
# )
