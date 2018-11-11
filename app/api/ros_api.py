# -*- coding: utf-8 -*-

import logging
import rospy
import os
import traceback
from flask import Blueprint, Flask, make_response, current_app, send_file
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
        traceback.print_exc()
        return ResponseModel.error(e.message)
    return ResponseModel.ok('launch start')


@api.route('/record', methods=['GET'])
def ros_record():
    try:
        RosCommon().record()
    except Exception, e:
        traceback.print_exc()
        return ResponseModel.error(e.message)
    return ResponseModel.ok('ros record done!')


@api.route('/close', methods=['GET', 'POST'])
def ros_record_close():
    while not rospy.is_shutdown():
        RosCommon().close()
    return ResponseModel.msg('ros record closed!')


@api.route('/download/<filename>', methods=['GET', 'POST'])
def download_ros_record_file(filename):
    log.info("start download file: {}".format(filename))

    try:
        bag_dir = current_app.config.get('BAG_DIR')
        file = os.path.join(app.root_path, bag_dir) + filename
        response = make_response(send_file(file))
        response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
        return response
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.message)


@api.route('/delete/<filename>', methods=['GET', 'POST'])
def delete_ros_file(filename):
    log.info("delete pcd file: {}".format(filename))
    try:
        bag_dir = current_app.config.get('BAG_DIR')
        file = os.path.join(app.root_path, bag_dir) + filename
        fileutil.delete(file)
        return ResponseModel.ok('done')
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.message)
        return ResponseModel.error(ex.message)


@api.route('/list', methods=['GET', 'POST'])
def get_record_files():
    bag_dir = current_app.config.get('BAG_DIR')
    return ResponseModel.ok(fileutil.get_ros_bag_files(bag_dir))
