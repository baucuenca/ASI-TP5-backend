# Modelo de prestamo de un libro, que involucra un libro y una miembro/socio

from sqlmodel import Field, SQLModel
from datetime import datetime

# Clase para el modelo de un prestamo en la BD
class Loan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id") # Clave foranea que asocia un libro (Book)
    member_id: int = Field(foreign_key="member.id") # Clave foranea que asocia un miembro (Member)
    loan_date: datetime = Field(default=datetime.now())
    return_date: datetime | None = Field(default=None)
    returned: bool = Field(default=False)

# Clase para crear un nuevo prestamo
class LoanCreate(SQLModel):
    book_id: int = Field(foreign_key="book.id") # Clave foranea que asocia un libro (Book)
    member_id: int = Field(foreign_key="member.id") # Clave foranea que asocia un miembro (Member)
    return_date: datetime | None = Field(default=None)

# Clase para actualizar un prestamo existente
class LoanUpdate(SQLModel):
    book_id: int | None = Field(default=None, foreign_key="book.id")
    member_id: int | None = Field(default=None, foreign_key="member.id")
    loan_date: datetime | None = Field(default=None)
    return_date: datetime | None = Field(default=None)
    returned: bool | None = Field(default=None)

# Clase para ver un prestamo
class LoanRead(SQLModel):
    book_title: str
    member_email: str
    loan_date: datetime
    return_date: datetime | None
    returned: bool