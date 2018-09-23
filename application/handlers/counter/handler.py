# -*- coding: utf-8 -*-

"""

计数器实现

:create: 2018/9/23
:copyright: smileboywtu

"""
import json
from operator import itemgetter

from jsonschema import validate, ValidationError

from application.base_handler import BaseHandler
from application.response import Response, ServerException, handle_exception
from common.redis_driver import RedisTK
from .validator import schemas


class CounterView(BaseHandler):

    async def validate_arguments(self, method, data):
        return validate(data, itemgetter(method.lower())(schemas))

    @handle_exception
    async def get(self, *args, **kwargs):
        """
        get counter number
        
        """
        if not self.request.body:
            raise ServerException("params_err", "need params")

        try:
            data = json.loads(self.request.body.decode())
        except:
            raise ServerException("params_err", "body need to be json")

        try:
            self.validate_arguments(self.request.method, data)
        except ValidationError as e:
            raise ServerException("params_err", str(e))

        cache = RedisTK()
        number = await cache.get(data["name"])
        self.json("success", data={
            "number": int(number)
        })


    async def post(self, *args, **kwargs):
        pass

    async def put(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass
