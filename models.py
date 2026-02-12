from pydantic import BaseModel
from typing import Optional, List


# Base properties shared across all schemas
class BookBase(BaseModel):
    # Making these Optional allows the API to handle the null values in your CSV
    author: Optional[str] = "Unknown Author"
    year: Optional[int] = 0
    publisher: Optional[str] = None
    image_url: Optional[str] = None


class BookCreate(BookBase):
    title: str
    isbn: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    image_url: Optional[str] = None


class BookResponse(BookBase):
    id: int
    title: str
    isbn: str

    # This allows Pydantic to convert SQLAlchemy objects to JSON automatically
    model_config = {
        "from_attributes": True
    }


class BookListResponse(BaseModel):
    total: int
    page: int
    limit: int
    books: List[BookResponse]


class DeleteResponse(BaseModel):
    message: str
    book: Optional[BookResponse] = None
