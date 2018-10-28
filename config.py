# -*- coding: utf-8 -*-

class Config:

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    BAG_DIR = '/data/'


class ProductionConfig(Config):
    BAG_DIR = '/data/'


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
