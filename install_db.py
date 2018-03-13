import os
import shutil

work_dir = os.path.dirname(os.path.realpath(__file__))
migration_dir = os.path.join(work_dir, 'pocket_monitor/db/migrations')
if os.path.exists(migration_dir):
    shutil.rmtree(migration_dir)
os.chdir(work_dir)
os.system('manage.py migrate & '
          'python manage.py makemigrations db & '
          'python manage.py migrate db')
