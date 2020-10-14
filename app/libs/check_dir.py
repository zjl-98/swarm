"""
 Created by zjl on 2020/9/26 12:26
"""
import os

__author__ = 'zjl'


def is_exists_dir(path):
    # 判断目录是否存在
    path = path.strip()
    path = path.rstrip('\\')

    is_exit = os.path.exists(path)
    if not is_exit:
        os.mkdir(path)


def take_exists_dir(dir_name, path):
    path = os.path.join(dir_name, path)
    is_exit = os.path.exists(path)
    if not is_exit:
        os.mkdir(path)


def is_exists_file(dir_path, filename):
    is_exists = os.path.exists(os.path.join(dir_path, filename))
    return True if is_exists else False


def join_path(dir_name, path):
    new_path = os.path.join(dir_name, path)
    return new_path