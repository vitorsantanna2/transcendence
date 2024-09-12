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

# Aplica as migrações do banco de dados
echo "Aplicando migrações do banco de dados..."
python ../mysite/manage.py migrate

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python ../mysite/manage.py collectstatic --noinput

# Inicia o servidor ASGI com Daphne
echo "Iniciando o servidor Daphne..."
daphne -b 0.0.0.0 -p 8001 mysite.asgi:application