#!/usr/bin/env bash
set -e

echo "[entrypoint] Esperando a MySQL (${MYSQL_HOST}:${MYSQL_PORT:-3306})..."
python - <<'PYCODE'
import os, time, sys
import pymysql

host = os.getenv("MYSQL_HOST","mysql")
port = int(os.getenv("MYSQL_PORT","3306"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

for i in range(30):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=2)
        conn.close()
        print("MySQL OK")
        break
    except Exception as e:
        print(f"Intento {i+1}/30: MySQL no responde aún ({e})")
        time.sleep(2)
else:
    print("ERROR: MySQL no disponible a tiempo", file=sys.stderr)
    sys.exit(1)
PYCODE

echo "[entrypoint] Aplicando migraciones Alembic..."
alembic upgrade head || {
  echo "Fallo migraciones"; exit 1;
}

echo "[entrypoint] Iniciando FastAPI (Uvicorn)..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000