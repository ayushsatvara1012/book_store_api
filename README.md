# Book Store API

A modular RESTful API built with FastAPI for managing a book collection. This project demonstrates a clean project structure separating concerns into routers, models, database logic, and exception handling.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete books.
- **Search**: Filter books by author and year.
- **In-Memory Database**: Uses a thread-safe list structure for storage.
- **Modular Design**: Code is organized into specific files for better maintainability.
- **Swagger UI**: Automatic interactive API documentation.

## Project Structure

```
/
├── main.py           # Application entry point & CORS config
├── database.py       # In-memory storage and ID generation logic
├── models.py         # Pydantic schemas for data validation
├── exceptions.py     # Custom error handling classes
└── routers/
    └── books.py      # API route handlers for book operations
```

## Installation

1. Ensure you have Python installed.
2. Install the required dependencies:

```bash
pip install fastapi uvicorn
```

## Running the Application

Run the server using `uvicorn` from the root directory:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Documentation
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Books
- `GET /books`: Get all books.
- `GET /books/{id}`: Get a specific book by ID.
- `GET /books/search/?author=...&year=...`: Search books by author or year.
- `POST /books`: Create a new book.
- `PUT /books/{id}`: Update an entire book.
- `PATCH /books/{id}`: Partially update a book.
- `DELETE /books/{id}`: Delete a specific book.
- `DELETE /books`: Delete all books.

## Usage Example (JSON)

**Create a Book:**
```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "year": 1925
}
```