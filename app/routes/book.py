# Endpoints para el modelo Libro

from fastapi import APIRouter, HTTPException, Response
from sqlmodel import select

from ..models.book import Book, BookCreate, BookUpdate
from ..models.loan import Loan
from ..config.db import session_dep

# Rutas
book = APIRouter()

# Obtener todos los libros
@book.get("/books", response_model=list[Book], tags=["Books"])
def read_books(session: session_dep):
    db_books = session.exec(select(Book)).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found")
    return db_books

# Obtener un libro por ID
@book.get("/books/{book_id}", response_model=Book, tags=["Books"])
def read_book(book_id: int, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Crear un nuevo libro
@book.post("/books", response_model=Book, tags=["Books"])
def create_book(book: BookCreate, session: session_dep):
    db_book = Book.model_validate(book) # Validar y crear instancia de Book lista para insertar en la BD
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# Actualizar un libro existente
@book.patch("/books/{book_id}", response_model=Book, tags=["Books"])
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

# Eliminar un libro existente
@book.delete("/books/{book_id}", status_code=204, tags=["Books"])
def delete_book(book_id: int, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Verificar que el libro no tiene un prestamo activo
    active_loan = session.exec(select(Loan).where(Loan.book_id == book_id, Loan.returned == False)).first()
    if active_loan:
        raise HTTPException(status_code=409, detail="Book is currently on loan") # Conflicto

    session.delete(db_book)
    session.commit()
    return Response(status_code=204) # Respuesta exitosa sin contenido