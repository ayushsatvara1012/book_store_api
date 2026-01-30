from fastapi import FastAPI
from routers import books
from fastapi.middleware.cors import CORSMiddleware
import database

app = FastAPI()
origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'],
                   allow_headers=['*'])
app.include_router(books.router)

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

# # -------------------------- Root Endpoint -------------------------- #
@app.get('/')
def root():
    return {
        "message": "Welcome to Book Store API!",
        "endpoints": {
            "Documentation": "/docs",
            "Books API": "/books"
            }
        }
