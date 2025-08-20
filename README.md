# ASI-TP5-backend

TP 5 (backend) - Administración de Sistemas de Información - UTN (FRLP)

## Para correr el proyecto:

### 1) Crear y activar un entorno virtual (venv).

- py -m venv .venv
- .venv\Scripts\activate

### 2) Instalar las dependencias dentro del entorno virtual.

- pip instal -r requirements.txt

### 3) Levantar la BD de MySQL en un contenedor Docker y acceder a su terminal.

- docker compose up -d
- docker exec -it asi-tp5-backend-mysql-1 bash
- mysql -p

## Migraciones

### 1) Para actualizar los modelos de datos en la BD (migraciones/migrations):

- alembic revision --autogenerate -m "Mensaje de la migracion"
- alembic upgrade head

### 2) Para deshacer la ultima migracion

- alembic downgrade -1
