#!/bin/sh

echo "Esperando banco ficar disponível..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco disponível."

echo "Rodando migrations..."
alembic upgrade head

echo "Rodando seeds..."
python -m app.seeds.run || true

echo "Subindo API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
