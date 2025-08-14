# Endpoints para el modelo Libro

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..models.book import Book
from ..config.db import session_dep

# Rutas
book = APIRouter()

@book.get("/books")
def read_books(session: session_dep):
    books = session.exec(select(Book)).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@book.get("/books/{book_id}")
def read_book(book_id: int, session: session_dep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book.post("/books")
def create_book(book: Book, session: session_dep):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book