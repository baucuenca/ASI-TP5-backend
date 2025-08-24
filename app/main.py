# Archivo principal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.book import book
from .routes.member import member
from .routes.loan import loan
from .config.db import create_tables, create_database

from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

origins = [
    FRONTEND_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book)
app.include_router(member)
app.include_router(loan)

@app.on_event("startup")
def startup_event():
    create_database() # Crea la base de datos si no existe
    # create_tables() # Crea las tablas en la base de datos. No es necesario si se utilizan migraciones para actualizar la BD