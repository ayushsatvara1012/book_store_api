from pydantic import BaseModel
from typing import Optional, List

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    
    model_config = {
        "from_attributes": True
    }

class DeleteResponse(BaseModel):
    message: str
    book: Optional[BookResponse] = None
