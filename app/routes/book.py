# Endpoints para el modelo Libro

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..models.book import Book, BookCreate, BookUpdate
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

# Actualizar un libro existente
@book.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)  # Excluir campos no enviados
    db_book.sqlmodel_update(book_data)  # Actualizar los campos del libro
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# Eliminar un libro
@book.delete("/books/{book_id}")
def delete_book(book_id: int, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"book_deleted": True}