# -*- coding: utf-8 -*-
from flask import Response, jsonify
from app.model import ResponseModel


class SteakResponse(Response):
    @classmethod
    def force_type(cls, ResponseModel, environ=None):
        if isinstance(Response, (list, dict, object)):
            response = jsonify(ResponseModel.serialze())
        return super(Response, cls).force_type(response, environ)
