# -*- coding: utf-8 -*-
import os
import shutil
import uuid

from flask import current_app


def new_tmp(file):
    """ 新建临时文件 """
    u = uuid.uuid1()
    name, ext = os.path.splitext(file.filename)
    filename = ''.join([u.hex, ext])
    path = "/".join([current_app.static_folder,
                     current_app.config["TMP_PATH"], filename])
    file.save(path)
    return (filename, name)


def enable_tmp(path, name):
    """ 激活临时文件 """
    filename = '/'.join([current_app.static_folder,
                         current_app.config["TMP_PATH"], name])
    if not os.path.exists(filename):
        return False
    _filename = '/'.join([current_app.static_folder, path, name])
    shutil.move(filename, _filename)
    return True


def delete_tmp(filename):
    path = current_app.config["TMP_PATH"]
    return delete_file(path, filename)


def delete_file(path, name):
    """ 删除文件 """
    filename = '/'.join([current_app.static_folder, path, name])
    if not os.path.exists(filename):
        return False
    os.remove(filename)
    return True


def delete(path):
    os.unlink(path)


def write(path, contents):
    with open(path, 'w') as handle:
        handle.write(contents)


def exists(path):
    return os.path.exists(path)


def listdir(dir):
    return os.listdir(dir)


def isfile(file):
    return os.path.isfile(file)


def get_ros_bag_files(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            result.append(f.name)
    print(result)
    return result
