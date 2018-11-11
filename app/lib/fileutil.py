# -*- coding: utf-8 -*-
import os
import time
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


def get_file_size(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 3)


def get_file_create_time(filePath):
    filePath = unicode(filePath, 'utf8')
    t = os.path.getctime(filePath)
    timeStruct = time.localtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def get_ros_bag_files(path):
    files = os.listdir(path)
    files.sort(key=lambda x:int(x[:-4]))
    result = []
    for file in files:
        file_path = os.path.join(path, file)
        if not os.path.isdir(file_path):
            if os.path.splitext(file_path)[1] == '.pcd':
                result.append({
                    'fileName': file,
                    'path': file_path,
                    'size': get_file_size(file_path),
                    'createTime': get_file_create_time(file_path)
                })
    print result
    return result
