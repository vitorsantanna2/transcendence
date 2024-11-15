FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3-dev build-essential libpcre3-dev libpq-dev openssl netcat-openbsd

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mysite /mysite/

COPY requirements/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# isso aqui é exclusivo pra mim, pois to rodando no windows
RUN apt-get install -y dos2unix && dos2unix /entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/mysite
ENV PYTHONBUFFERED=1

ENTRYPOINT ["/entrypoint.sh"]