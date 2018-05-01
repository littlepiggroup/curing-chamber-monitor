import os

work_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(work_dir)
os.system('sqlite_web db.sqlite3')
