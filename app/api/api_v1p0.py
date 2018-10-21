# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, Flask
import logging
from app.exceptions import NoJsonException
api = Blueprint(name='api_v1p0', import_name=__name__, url_prefix="/api/v1.0")
log = logging.getLogger(__name__)


def validate_json(json):
    if not json or not hasattr(json, 'items'):
        raise NoJsonException()


@api.route('/test', methods=['GET'])
def get_todo_list():
    test = {"test": "aaa"}
    return jsonify(test)
