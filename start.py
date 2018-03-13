import os
import subprocess

work_dir = os.path.dirname(os.path.realpath(__file__))
subprocess.Popen("python manage.py runserver 0.0.0.0:8000", shell=True, cwd=work_dir).communicate()
