# -*- coding: utf-8 -*-

from .logging import Logging

logging = Logging()


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            logging,
    ):
        extension.init_app(app)
