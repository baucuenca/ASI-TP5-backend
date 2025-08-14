# Modelo de libro

from sqlmodel import Field, SQLModel
from typing import Optional 
from datetime import datetime

# Clase para el modelo de datos del libro en la BD
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)

# Clase para la creación de un nuevo libro
class BookCreate(SQLModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)
