# -*- coding: utf-8 -*-

"""


:create: 2018/9/23
:copyright: smileboywtu

"""

from asyncio import Future
from unittest import mock

from tornado.testing import AsyncHTTPSTestCase

from application.app import make_app


class BaseTestCase(AsyncHTTPSTestCase):
    """
    测试用例类, 启动服务并执行测试. 接口与父类`AsyncHTTPSTestCase`一致
    """

    def customer_settings(self):
        return {
            "cookie_secret": "example"
        }

    def get_app(self):
        """
        模拟start.py创建app并添加配置
        :return: 
        """

        settings = self.customer_settings()
        app = make_app(settings["cookie_secret"])
        app.settings.update(settings)
        return app

    def get_new_ioloop(self):
        """
        所有test使用一个IOLoop
        :return: 
        """
        from tornado.ioloop import IOLoop
        return IOLoop.current()

    def setUp(self):
        """
        `self._patcher`用于在`TestCase`类中创建patcher后, 能够被`tearDown()`回收.
        """
        AsyncHTTPSTestCase.setUp(self)
        self._patcher = []
        self.default_mock()

    def tearDown(self):
        """
        回收patcher
        :return: 
        """
        AsyncHTTPSTestCase.tearDown(self)
        for patcher in self._patcher:
            patcher.stop()

    def _mock_future(self, method, return_value):
        """
        Mock 协程/Future对象
        :param method: 需要被 mock 的方法
        :param return_value: 期望的返回值
        :return: 
        """
        _patcher = mock.patch(method)
        ft = Future()
        ft.set_result(return_value)
        self._patcher.append(_patcher)
        mocker = _patcher.start()
        mocker.return_value = ft
        return mocker

    def default_mock(self):
        pass
