FROM python:2.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --update --no-cache \
    postgresql-dev \
    bash

COPY requirements.txt .

RUN apk add --update --no-cache --virtual=build-dependencies \
    build-base \
    git \
    && pip install -r requirements.txt \
    && apk del build-dependencies \
    && rm -rf /var/cache/apk/*

COPY webapps /app
COPY www /www

RUN mkdir logs
COPY docker-entrypoint.sh /app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
