import os

import time


def create_sub_dirs(base_dir, sub_path):
    import re
    normal_base_dir = re.sub(r'/$', '', base_dir)
    normal_sub_path = re.sub(r'^/', '', sub_path)
    abs_path = normal_base_dir + '/' + normal_sub_path

    if not os.path.isdir(normal_base_dir):
        # Try my best to create the base_dir firstly.
        os.mkdir(normal_base_dir)

    for part in normal_sub_path.split('/'):
        normal_base_dir += '/' + part
        if not os.path.isdir(normal_base_dir):
            os.mkdir(normal_base_dir)


def create_folders_for_project(project_info, base_dir):
    pass


def remove_old_files(dir_path, days):
    for f in os.listdir(dir_path):
        my_file = os.path.join(dir_path, f)
        if os.stat(my_file).st_mtime < time.time() - days * 86400:
            if os.path.isfile(my_file):
                os.remove(my_file)


if __name__ == '__main__':
    # create_sub_dirs('/home/jichao/', 'he/xx/xxss/xxx')
    remove_old_files('/home/jichao/Downloads', 3)