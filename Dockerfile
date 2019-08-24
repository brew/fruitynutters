FROM python:2.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --update --no-cache \
    postgresql-dev

COPY requirements.txt .

RUN apk add --update --no-cache --virtual=build-dependencies \
    build-base \
    git \
    && pip install -r requirements.txt \
    && apk del build-dependencies \
    && rm -rf /var/cache/apk/*

COPY webapps /app
COPY www /www

RUN ./manage.py collectstatic --no-input \
    && rm -rf /www

EXPOSE 8000

CMD ["gunicorn", "--chdir", "fruitynutters", "--bind", ":8000", "fruitynutters.wsgi:application"]
