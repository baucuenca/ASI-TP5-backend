# ASI-TP5-backend

TP 5 (backend) - Administración de Sistemas de Información - UTN (FRLP)

## Para correr el proyecto:

### 1) Crear y activar un entorno virtual (venv).

py -m venv .venv
.venv\Scripts\activate

### 2) Instalar las dependencias dentro del entorno virtual.

pip instal -r requirements.txt

### 3) Levantar la BD de MySQL en un contenedor Docker.

docker compose up -d
