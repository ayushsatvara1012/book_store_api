from models import BookCreate, BookUpdate, BookResponse, DeleteResponse
from fastapi import APIRouter
from typing import List, Optional
from exceptions import BookNotFoundError
from database import Books_DB, get_new_id, reset_db_state

router = APIRouter(
    prefix='/books',
    tags=['Books']
    )

# -------------------------- Helper Functions -------------------------- #

def find_book_by_id(book_id: int):
    """Find the book by its ID"""
    for book in Books_DB:
        if book['id'] == book_id:
            return book
    return None

def find_book_index_by_id(book_id: int):
    """Find the index of the book by ID"""
    for index, book in enumerate(Books_DB):
        if book['id'] == book_id:
            return index
    return None

# -------------------------- Routes -------------------------- #

# -------------------------- Get All Books -------------------------- #
@router.get('', response_model=List[BookResponse])
def get_all_books():
    return Books_DB

# -------------------------- Search Books -------------------------- #
@router.get('/search/', response_model=List[BookResponse])
def search_book(author: Optional[str] = None, year: Optional[int] = None):
    result = Books_DB.copy()
    if author:
        result = [book for book in result if author.lower() in book['author'].lower()]
    if year:
        result = [book for book in result if year == book['year']]
    return result

# -------------------------- Get Single Book -------------------------- #
@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int):
    book = find_book_by_id(book_id)
    if not book:
        raise BookNotFoundError(book_id)
    return book

# -------------------------- Create Book -------------------------- #
@router.post('', status_code=201, response_model=BookResponse)
def create_book(book_create: BookCreate):
    new_id = get_new_id()
    new_book = {
        'id': new_id,
        **book_create.model_dump()
        }
    Books_DB.append(new_book)
    return new_book

# -------------------------- Update Book -------------------------- #
@router.put('/{book_id}', response_model=BookResponse)
def update_book(book_id: int, book: BookCreate):
    index = find_book_index_by_id(book_id)
    if index is None:
        raise BookNotFoundError(book_id)
    updated_book = {
        'id': book_id,
        **book.model_dump()
        }
    Books_DB[index] = updated_book
    return updated_book

# -------------------------- Partial Update -------------------------- #
@router.patch('/{book_id}', response_model=BookResponse)
def partial_book_update(book_id: int, book_update: BookUpdate):
    book = find_book_by_id(book_id)
    if not book:
        raise BookNotFoundError(book_id)
    updated_data = book_update.model_dump(exclude_unset=True)
    for key, val in updated_data.items():
        book[key] = val
    return book

# -------------------------- Delete Book -------------------------- #
@router.delete('/{book_id}', response_model=DeleteResponse)
def delete_book(book_id: int):
    index = find_book_index_by_id(book_id)
    if index is None:
        raise BookNotFoundError(book_id)
    deleted_book = Books_DB.pop(index)
    return {
        'message': 'Book Deleted Successfully !!',
        'book': deleted_book
        }

# -------------------------- Delete All Books -------------------------- #
@router.delete('', response_model=DeleteResponse)
def delete_all_books():
    count = len(Books_DB)
    Books_DB.clear()
    reset_db_state()
    return {
        'message': f'{count} Books Deleted Successfully !!',
        'book': None
        }
