#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrations ccmapp
python manage.py migrate
python manage.py crontab remove
python manage.py crontab add
python manage.py runserver
