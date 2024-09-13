#!/bin/sh

# Verifica se as variáveis de ambiente estão definidas
if [ -z "$DB_HOST" ]; then
  echo "A variável DB_HOST não está definida. Definindo para 'db'."
  DB_HOST=db
fi

if [ -z "$DB_PORT" ]; then
  echo "A variável DB_PORT não está definida. Definindo para '5432'."
  DB_PORT=5432
fi

# Espera até que o banco de dados esteja disponível
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Aguardando o banco de dados na porta $DB_PORT..."
  sleep 1
done

echo "Aplicando migrações do banco de dados..."
python ../mysite/manage.py migrate

echo "Coletando arquivos estáticos..."
python ../mysite/manage.py collectstatic --noinput

echo "Iniciando o servidor Daphne..."
python ../mysite/manage.py runserver 0.0.0.0:8001