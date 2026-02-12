from models import BookCreate, BookUpdate, BookResponse, DeleteResponse, BookListResponse
from fastapi import APIRouter, Depends, Query
from typing import Any, List, Optional
from exceptions import BookNotFoundError
from database import get_db, Book
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/books',
    tags=['Books']
)


# -------------------------- Routes -------------------------- #

# -------------------------- Get All Books -------------------------- #
@router.get('', response_model=BookListResponse)
def get_all_books(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(10, le=100)):
    skip = (page - 1) * limit
    total_count = db.query(Book).count()
    books = db.query(Book).offset(skip).limit(limit).all()
    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "books": books
    }

# -------------------------- Search Books -------------------------- #
@router.get('/search/', response_model=List[BookResponse])
def search_book(author: Optional[str] = None, year: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if author:
        # ILIKE is for case-insensitive search in PostgreSQL
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(Book.year == year)
    return query.all()

# -------------------------- Get Single Book -------------------------- #
@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)
    return book

# -------------------------- Create Book -------------------------- #
@router.post('', status_code=201, response_model=BookResponse)
def create_book(book_create: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book_create.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# -------------------------- Update Book -------------------------- #
@router.put('/{book_id}', response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    book_query = db.query(Book).filter(Book.id == book_id)
    book = book_query.first()
    if not book:
        raise BookNotFoundError(book_id)

    book_query.update(book_update.model_dump())
    db.commit()
    return book_query.first()

# -------------------------- Partial Update -------------------------- #
@router.patch('/{book_id}', response_model=BookResponse)
def partial_book_update(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)

    updated_data = book_update.model_dump(exclude_unset=True)
    for key, val in updated_data.items():
        setattr(book, key, val)

    db.commit()
    db.refresh(book)
    return book

# -------------------------- Delete Book -------------------------- #
@router.delete('/{book_id}', response_model=DeleteResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)

    db.delete(book)
    db.commit()
    return {
        'message': 'Book Deleted Successfully !!',
        'book': book
        }

# -------------------------- Delete All Books -------------------------- #
@router.delete('', response_model=DeleteResponse)
def delete_all_books(db: Session = Depends(get_db)):
    count = db.query(Book).delete()
    db.commit()
    return {
        'message': f'{count} Books Deleted Successfully !!',
        'book': None
        }
