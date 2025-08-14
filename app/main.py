# Archivo principal

from fastapi import FastAPI

from .routes.book import book
from .config.db import create_tables, create_database

app = FastAPI()

app.include_router(book)

@app.on_event("startup")
def startup_event():
    create_database()
    create_tables()