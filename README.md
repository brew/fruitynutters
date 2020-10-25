# Fruity Nutters food cooperative

This is an old, old project, running on the Django framework (started in 2008 just as Django version 1.0 was released!), so it's quite crusty. But it handles each member's food order, and makes it marginally easier for the sterling team of volunteers to collate and submit the massive collective order that results.

I've updated it to a more recent version of Django, so it's a little easier to maintain, and worked out a few of the most egregious kinks (though I'm sure there are still many horrors within).

So, if you want to run a food coop in _exactly the same way_ we do, then this is the old, crusty codebase for you!

## Docker

A Dockerfile is provided to build the Django app served by gunicorn. This image can be used for deployment with the provided docker-compose.yml file, which includes a Postgres database and nginx proxy server (which also serves the static images).

### Config

Provide the following config settings, either in an `.env` file, or as environmental variables:

```ini
# app
DEBUG=False
INTERNAL_IPS=(127.0.0.1)
ALLOWED_HOSTS=(.mygreatfoodcoopwebsite.org.uk,localhost)
DATABASE_URL=postgres://dbuser:secret@db:5432/postgres
SECRET_KEY='so-secret'
EMAIL_URL=smtp://myemailuser:myemailpassword@smtp.example.com:587
DJANGO_ADMINS=Fred Smith:fredsmith@example.com
ORDER_FORM_SEND_EMAIL='mailbot@example.com'
ORDER_FORM_REPLY_TO_EMAIL='friendly_volunteer@example.com'
GANALYTICS_TRACKING_CODE='U-XXXXX-ETC'

# db
POSTGRES_PASSWORD=secret
POSTGRES_USER=dbuser
POSTGRES_DB=postgres
```

### The database

The docker-compose file defines a Postgres database service. Its data directory is mapped to the host filesystem, relative to the docker-compose file at `./volumes/db`.

### Static assets and media

The Django app's static assets and media files are also mapped to directories in the host filesystem: `./volumes/static` and `./volumes/media`. These are mounted into the Django app and Nginx services. Static assets are generated during startup by the Django app service using `collectstatic`. Nginx will service these static assets directly.

### Production

Ensure there's `.env.prod` file set out as above.

Run:

```sh
docker-compose -f docker-compose.prod.yml --env-file ./.env.prod up --build -d
```
