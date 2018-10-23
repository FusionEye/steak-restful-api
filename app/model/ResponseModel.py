# -*- coding: utf-8 -*-


class ResponseModel(object):

    def __init__(self, result={}, message='Success', success=True):
        self.message = message
        self.result = result
        self.success = success

    def serialze(self):
        dict = self.__dict__
        print dict
        return dict


def ok(result):
    return ResponseModel(result)


def error(result):
    return ResponseModel(result, 'Error', False)


def msg(message):
    print message
    return ResponseModel(message=message)
