FROM python:3.11-alpine

RUN mkdir /code
WORKDIR /code
COPY ../../ /code/
# uwsgi setup
RUN apk add python3-dev build-base linux-headers pcre-dev libpq-dev
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "/code/core.uwsgi.ini"]