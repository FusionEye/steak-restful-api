# -*- coding: utf-8 -*-

from flask import make_response
from app import create_app
from app.api import ros_api, SteakResponse
from app.logging import Logging
from app.exceptions import *
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
app.response_class = SteakResponse
app.register_blueprint(ros_api.api)


@app.errorhandler(NotFoundException)
@app.errorhandler(404)
def not_found(error):
    msg = error.msg if hasattr(error, 'msg') else 'Not found'
    return make_response('{"error": "%s"}' % msg, 404)


@app.errorhandler(DatabaseValidationException)
@app.errorhandler(NoJsonException)
@app.errorhandler(400)
def bad_request(error):
    msg = 'Bad request'
    if hasattr(error, 'msg'):
        msg = error.msg
    elif hasattr(error, 'description') and error.description.startswith('Failed to decode JSON'):
        msg = 'Invalid JSON'
    return make_response('{"error": "%s"}' % msg, 400)


if __name__ == '__main__':
    Logging.init_app('./log/app')
    Logging.init_app('./log/app', app.logger)
    app.run()
