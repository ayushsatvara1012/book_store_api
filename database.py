from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

# URL encode the password to handle special characters like '@'
password = urllib.parse.quote_plus("ayush@postgre123")
DATABASE_URL = f'postgresql://postgres:{password}@localhost:5432/bookstore'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# -------------------------- Database Models -------------------------- #

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    year = Column(Integer)

# -------------------------- Dependency -------------------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
