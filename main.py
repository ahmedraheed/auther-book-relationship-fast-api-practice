from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine
from models import Base
from schemas import AuthorCreate, BookCreate
from crud import create_author, add_book_to_author, get_books_by_author
from database import get_db

# Initialize the app and create tables
app = FastAPI()
Base.metadata.create_all(bind=engine)



@app.post("/authors", response_model=dict)
def create_author_endpoint(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = create_author(db, author.name)
    return {"message": "Author created successfully", "author": {"id": new_author.id, "name": new_author.name}}

@app.post("/authors/{author_id}/books", response_model=dict)
def add_book_endpoint(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    new_book = add_book_to_author(db, author_id, book.title)
    if not new_book:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Book added successfully", "book": {"id": new_book.id, "title": new_book.title}}

@app.get("/authors/{author_id}/books", response_model=dict)
def get_books_by_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    books = get_books_by_author(db, author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    book_list = [{"id": book.id, "title": book.title} for book in books]
    return {"author_id": author_id, "books": book_list}
