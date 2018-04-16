#!/usr/bin/env bash
# sudo apt-get install mysql-server
# sudo apt-get install python-dev
# sudo apt-get install libmysqlclient-dev

pip install -r requirements.txt
python manage.py migrate auth
python manage.py makemigrations ccmapp
python manage.py migrate
# install create_views.sql after migrate
python manage.py crontab remove
python manage.py crontab add
python manage.py runserver
