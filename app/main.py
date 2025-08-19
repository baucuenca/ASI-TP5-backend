# Archivo principal

from fastapi import FastAPI

from .routes.book import book
from .routes.member import member
from .routes.loan import loan
from .config.db import create_tables, create_database

app = FastAPI()

app.include_router(book)
app.include_router(member)
app.include_router(loan)

@app.on_event("startup")
def startup_event():
    create_database() # Crea la base de datos si no existe
    # create_tables() # Crea las tablas en la base de datos. No es necesario si se utilizan migraciones para actualizar la BD