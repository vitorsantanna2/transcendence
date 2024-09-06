FROM python:3.10.12-alpine

RUN mkdir /code
WORKDIR /code

COPY ../../ /code/

ENV PYTHONPATH=/code

RUN apk add python3-dev build-base linux-headers pcre-dev libpq-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["gunicorn", "wsgi: mysite.wsgi", "--bind", "0.0.0.0:8000"]