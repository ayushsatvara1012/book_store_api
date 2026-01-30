from fastapi import HTTPException

class BookNotFoundError(HTTPException):
    def __init__(self, book_id: int):
        super().__init__(
            status_code=404,
            detail=f'Book ID: {book_id} Not found !! Please Try Again !!!'
            )
