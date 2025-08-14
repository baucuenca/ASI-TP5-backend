# Endpoints para el modelo Libro

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..models.book import Book, BookCreate
from ..config.db import session_dep

# Rutas
book = APIRouter()

# Obtener todos los libros
@book.get("/books")
def read_books(session: session_dep):
    books = session.exec(select(Book)).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# Obtener un libro por ID
@book.get("/books/{book_id}")
def read_book(book_id: int, session: session_dep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Crear un nuevo libro
@book.post("/books")
def create_book(book: BookCreate, session: session_dep):
    db_book = Book.model_validate(book) # Validar y crear instancia de Book lista para insertar en la BD
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book