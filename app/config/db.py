# Conexion a la BD

import os
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel, text
from dotenv import load_dotenv
from typing import Annotated

# Cargar variables de entorno
load_dotenv()

MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT = os.getenv("MYSQL_PORT")

# URL de conexion
database_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(database_url)

server_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:{MYSQL_PORT}/"
server_engine = create_engine(server_url)

# Crear la BD si no existe
def create_database():
    server_engine = create_engine(server_url)
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
    server_engine.dispose()

# Crear las tablas
def create_tables():
    SQLModel.metadata.create_all(engine)

# Sesión de la BD
def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]