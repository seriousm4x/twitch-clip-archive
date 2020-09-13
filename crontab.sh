#!/bin/bash

/home/max/git/django-twitch-archive/.venv/bin/python /home/max/git/django-twitch-archive/manage.py updateDB && \
/home/max/git/django-twitch-archive/.venv/bin/python /home/max/git/django-twitch-archive/manage.py download && \
/home/max/git/django-twitch-archive/.venv/bin/python /home/max/git/django-twitch-archive/manage.py collectstatic --noinput
