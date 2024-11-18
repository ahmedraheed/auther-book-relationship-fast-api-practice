from sqlalchemy.orm import Session
from models import Author, Book

def create_author(db: Session, name: str):
    new_author = Author(name=name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def add_book_to_author(db: Session, author_id: int, title: str):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        return None
    new_book = Book(title=title, author_id=author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_books_by_author(db: Session, author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        return None
    books = db.query(Book).filter(Book.author_id == author_id).all()
    return books
