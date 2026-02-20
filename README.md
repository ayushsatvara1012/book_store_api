# Book Store API - LuminaLib (backend code)

## Project Overview
The Book Store API is a RESTful service that allows users to manage a collection of books. It provides features for adding, updating, deleting, and retrieving book information through a set of well-defined endpoints.

## Installation Instructions
1. Clone this repository:
   ```
   git clone https://github.com/ayushsatvara1012/book_store_api.git
   ```

2. Change the directory:
   ```
   cd book_store_api
   ```

3. Install the dependencies:
   ```
   npm install
   ```

4. Start the server:
   ```
   npm start
   ```

## API Endpoints
- **GET /api/books**: Retrieve a list of all books.
- **GET /api/books/:id**: Retrieve a single book by ID.
- **POST /api/books**: Add a new book to the collection.
- **PUT /api/books/:id**: Update an existing book by ID.
- **DELETE /api/books/:id**: Remove a book from the collection.

## Usage Examples
### Retrieve All Books
```bash
curl -X GET http://localhost:3000/api/books
```

### Add a New Book
```bash
curl -X POST http://localhost:3000/api/books -H "Content-Type: application/json" -d '{"title": "New Book", "author": "Author Name", "price": 20.99}'
```

### Update a Book
```bash
curl -X PUT http://localhost:3000/api/books/1 -H "Content-Type: application/json" -d '{"title": "Updated Book", "author": "New Author Name", "price": 15.99}'
```

### Delete a Book
```bash
curl -X DELETE http://localhost:3000/api/books/1
```
