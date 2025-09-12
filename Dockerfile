# Usar una imagen base oficial de Python
FROM python:3.13-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Dar permiso al entrypoint
RUN chmod +x /app/entrypoint.sh

# Puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["./entrypoint.sh"]