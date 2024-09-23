FROM python:3.11-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN apk update && apk add --no-cache \
	python3-dev \
	build-base \
	linux-headers \
	pcre-dev \
	libpq-dev \
	openssl

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

RUN pip install uwsgi

RUN python manage.py migrate

CMD ["uwsgi", "--ini", "base.uwsgi.ini"]