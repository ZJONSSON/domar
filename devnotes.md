# Env variables

Keep env variables in your local .env file

A template is provided: .env_tmp


# PostgreSQL

We use (for now) PostgreSQL 9.6 - install it for your operating system

Create a database (named 'lagagogn'). Create a user (let's call it lagagogn) with a password (and set it in your .env).

Also in a psql prompt:

`ALTER ROLE lagagogn SET client_encoding TO 'utf8';`

`ALTER ROLE lagagogn SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE lagagogn SET timezone TO 'UTC';`

`GRANT ALL PRIVILEGES ON DATABASE lagagogn TO lagagogn;`


# Django

First of all, apply the initial migrations (from the lagagogn-django directory):

`python manage.py migrate`

then create a superuser:

`python manage.py createsuperuser`

and then run the devserver:

`python manage.py runserver`
