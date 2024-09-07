FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3-dev build-essential libpcre3-dev libpq-dev openssl

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mysite /mysite/
COPY requirements/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/mysite

ENTRYPOINT ["/entrypoint.sh"]