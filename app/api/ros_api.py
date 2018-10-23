# -*- coding: utf-8 -*-

import logging
import rospy
from flask import Blueprint, Flask, send_from_directory

from app.exceptions import NoJsonException
from app.lib import rosutil, fileutil
from app.model import ResponseModel

app = Flask(__name__)
api = Blueprint(name='api_ros', import_name=__name__, url_prefix="/api/ros")
log = logging.getLogger(__name__)


def validate_json(json):
    if not json or not hasattr(json, 'items'):
        raise NoJsonException()


@api.route('/record', methods=['GET'])
def ros_record():
    test = {"test": "aaa"}
    return ResponseModel.ok(test)


@api.route('/close', methods=['GET', 'POST'])
def ros_record_close():
    while not rospy.is_shutdown():
        rosutil.close()
    return ResponseModel.msg('ros record closed!')


@api.route('/download/<filename>', methods=['GET', 'POST'])
def download_ros_record_file(filename):
    dirpath = os.path.join(app.root_path, 'upload')
    return send_from_directory(dirpath, filename, as_attachment=True)


@api.route('/list', methods=['GET', 'POST'])
def get_record_files():
    return ResponseModel.ok(fileutil.get_ros_bag_files('/data'))
