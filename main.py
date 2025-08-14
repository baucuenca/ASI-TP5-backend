import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, create_engine, select, SQLModel
from typing import Annotated

# Cargar variables de entorno
load_dotenv()

MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT = os.getenv("MYSQL_PORT")

# Conexion a la BD
database_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(database_url)

# Creacion de la BD y tablas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Obtener una sesión de la BD
def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

# Models
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True) # el index=True indica que se creará un índice en esta columna, para mejorar la búsqueda

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "hello wrld"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Endpoints de la API
@app.post("/books/")
def create_book(book: Book, session: session_dep):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/")
def read_books(session: session_dep):
    books = session.exec(select(Book)).all()
    return books

@app.get("/books/{book_id}")
def read_book(book_id: int, session: session_dep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}")
def update_book(book_id: int, book: Book, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    hero_data = book.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(hero_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: session_dep):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"msg": "Book deleted"}