# Modelo de miembro o socio de la biblioteca

from sqlmodel import Field, SQLModel
from datetime import datetime

# Clase para el modelo de datos del miembro en la BD
class Member(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15) 
    joined_date: datetime = Field(default=datetime.now()) # Fecha de creacion
    is_active: bool = Field(default=True)  # Estado del miembro: activo o inactivo

# Clase para la creación de un nuevo miembro
class MemberCreate(SQLModel):
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)

# Clase para la actualización de un miembro existente
class MemberUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=15)
