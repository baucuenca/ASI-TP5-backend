# Modelo Libro

from sqlmodel import Field, SQLModel
from typing import Optional 
from datetime import datetime

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)

class BookCreate(SQLModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    published_year: int = Field(default=datetime.now().year)
    isbn: str = Field(max_length=13)
