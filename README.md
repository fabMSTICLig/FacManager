# FacManager
Code developments under license GPL-3.0


A web application in order to manage the reservation of the machines and the manager of a university fablab

## Installation

### Prerequisite
- Python 3
- Node JS

### Backend Step Django

```
$ cd facmanager
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ mkdir config
$ # add a secret key in config/secretkey.txt example of generator https://djecrety.ir/
$ edit config/secretkey.txt
$ cp facmanager/local_settings.py.example facmanager/local_settings.py
$ # modify facmanager/local_settings.py to your need
$ edit facmanager/local_settings.py
$ python manage.py migrate
```

### Frontend Step VueJS

```
$ cd facmanager/frontend
$ npm install
$ cp .env.local.example .env.local
$ # edit .env.local to your need
$ edit .env.local
```

You must provide a src/pages/LegalNotice.vue file. This file must contain the legal notice for your site. It is a HTML file with `<template>` as root node.

You must provide a src/pages/HomeTop.vue file. This file must contain informations you want to show on the Home page. It is a HTML file with `<template>` as root node.


```
$ # in frontend folder
$ npm run build
```

### Add the superuser

You have two choice. Create a new superuser or login with alternative login backend such as CAS and setting it to superuser.

Create a super user

```
$ python manage.py createsuperuser
```

Set a user to superuser

```
$ python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> u = User.objects.get(username="THEUSERNAME")
>>> u.is_superuser=True
>>> u.is_staff=True
>>> u.save()
>>> exit()
```

## Deployement

Exemple of startup script

```
#!/bin/bash
. /var/resa/facmanager/venv/bin/activate
cd /var/resa/facmanager
gunicorn facmanager.wsgi:application --bind=0.0.0.0:8000
```

Then use a reverse proxy to serve the web app such as Nginx or Apache

Dont forget to serve the static directory `/path/to/facmanager/static/`


