# -*- coding: utf-8 -*-

import logging
import rospy
import os
from flask import Blueprint, Flask, send_from_directory, current_app
from app.lib import fileutil
from app.exceptions import NoJsonException
from app.lib.ros import RosCommon
from app.model import ResponseModel

app = Flask(__name__)
api = Blueprint(name='api_ros', import_name=__name__, url_prefix="/api/ros")
log = logging.getLogger(__name__)


def validate_json(json):
    if not json or not hasattr(json, 'items'):
        raise NoJsonException()


@api.route('/launch/start', methods=['GET', 'POST'])
def ros_launch_start():
    try:
        RosCommon().launch_start('test.launch')
    except Exception, e:
        return ResponseModel.error(e.message)
    return ResponseModel.ok('launch start')


@api.route('/record', methods=['GET'])
def ros_record():
    try:
        RosCommon().record()
    except Exception, e:
        return ResponseModel.error(e.message)
    return ResponseModel.ok('ros record done!')


@api.route('/close', methods=['GET', 'POST'])
def ros_record_close():
    while not rospy.is_shutdown():
        RosCommon().close()
    return ResponseModel.msg('ros record closed!')


@api.route('/download/<filename>', methods=['GET', 'POST'])
def download_ros_record_file(filename):
    bag_dir = current_app.config.get('BAG_DIR')
    dirpath = os.path.join(app.root_path, bag_dir)
    return send_from_directory(dirpath, filename, as_attachment=True)


@api.route('/list', methods=['GET', 'POST'])
def get_record_files():
    bag_dir = current_app.config.get('BAG_DIR')
    return ResponseModel.ok(fileutil.get_ros_bag_files(bag_dir))
