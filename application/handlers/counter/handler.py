# -*- coding: utf-8 -*-

"""

计数器实现

:create: 2018/9/23
:copyright: smileboywtu

"""
from operator import itemgetter

from jsonschema import validate, ValidationError

from application.base_handler import BaseHandler
from application.response import ServerException, handle_exception
from common.redis_driver import RedisTK
from common.utils import decode_to_string
from .validator import schemas


class CounterView(BaseHandler):

    def validate_arguments(self, method, data):
        return validate(data, itemgetter(method.lower())(schemas))

    @handle_exception
    async def get(self, *args, **kwargs):
        """
        get counter number
        
        """
        if not self.request.query_arguments:
            raise ServerException("params_err", "need params")

        data = decode_to_string(self.request.query_arguments)

        try:
            self.validate_arguments(self.request.method, data)
        except ValidationError as e:
            raise ServerException("params_err", str(e))

        print(data)

        cache = RedisTK()
        number = await cache.get(data["name"]) or 0
        self.json("success", data={
            "number": int(number)
        })

    async def post(self, *args, **kwargs):
        pass

    async def put(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass
