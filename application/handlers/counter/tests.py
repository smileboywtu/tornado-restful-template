# -*- coding: utf-8 -*-

"""

counter 测试用例

:create: 2018/9/23
:copyright: smileboywtu

"""
import json
from unittest import mock

from jsonschema import validate, ValidationError
from tornado.httputil import url_concat

from tests.base_testcase import BaseTestCase
from .validator import schemas


class CounterTC(BaseTestCase):
    def mock_redis_class(self):
        class FutureDict():
            def __init__(self, data):
                self.__data = data

            async def get(self, key):
                return self.__data.get(key)

        patcher = mock.patch("application.handlers.counter.handler.RedisTK", return_value=FutureDict({
            "zhangsan": 1
        }))
        self._patcher.append(patcher)
        patcher.start()
        return patcher

    def test_counter_get(self):
        self.mock_redis_class()
        params = {
            "name": "zhangsan"
        }
        url = url_concat("/api/v1/counter", params)
        response = self.fetch(url, method="GET", headers={'Origin': "test"})

        print(response.body)
        self.assertEqual(response.code, 200, msg="请求异常, status_code: {}".format(response.code))
        rjson = json.loads(response.body.decode())
        self.assertEqual(rjson["code"], 0, msg="请求异常")

    def test_validate_get(self):
        data = {
            "name": 132
        }
        with self.assertRaises(ValidationError):
            validate(data, schemas["get"])

        data = {
            "name": "zhangsan"
        }
        validate(data, schemas["get"])
