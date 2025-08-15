# Modelo de libro

from sqlmodel import Field, SQLModel
from datetime import datetime

# Clase para el modelo de datos del libro en la BD
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)

# Clase para la creación de un nuevo libro
class BookCreate(SQLModel):
    title: str = Field(max_length=100)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)

# Clase para la actualización de un libro existente
class BookUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=100)
    author: str | None = Field(default=None, max_length=50)
    published_year: int | None = Field(default=None)
    isbn: str | None = Field(default=None, max_length=13)