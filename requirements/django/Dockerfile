FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y python3-dev build-essential libpcre3-dev libpq-dev openssl

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mysite /mysite/

COPY requirements/django/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/mysite
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/entrypoint.sh"]