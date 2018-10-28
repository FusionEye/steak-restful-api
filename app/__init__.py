# -*- coding: utf-8 -*-

from .logging import Logging
from flask import Flask
from config import config

logging = Logging()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    return app