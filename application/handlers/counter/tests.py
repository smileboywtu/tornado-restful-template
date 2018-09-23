# -*- coding: utf-8 -*-

"""

counter 测试用例

:create: 2018/9/23
:copyright: smileboywtu

"""
import json
from unittest import mock

from jsonschema import validate, ValidationError

from tests.base_testcase import BaseTestCase
from .validator import schemas


class CounterTC(BaseTestCase):
    def mock_redis_class(self):
        patcher = mock.patch("application.handlers.counter.handler.RedisTK", return_value={
            "zhangsan": 1
        })
        self._patcher.append(patcher)
        patcher.start()
        return patcher

    def test_counter_get(self):
        self.mock_redis_class()
        data = json.dumps({
            "name": "zhangsan"
        })

        response = self.fetch("/api/v1/counter", method="GET", body=data, headers={'Origin': "test"})

        print(response.body)
        self.assertEqual(response.code, 200, msg="请求异常, status_code: {}".format(response.code))
        rjson = json.loads(response.body.decode())
        self.assertEqual(rjson["status"], 0, msg="请求异常")

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
