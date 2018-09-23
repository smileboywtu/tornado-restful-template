# -*- coding: utf-8 -*-

"""

web request 处理基类

:create: 2018/9/23
:copyright: smileboywtu

"""
from tornado.web import RequestHandler

from application.response import Response
from common.loggers import with_request_id, RequestIDContext


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_header()
        self._set_ssl()

    @with_request_id
    async def initialize(self):
        """
        make the request id context is available
        
        :return: 
        """
        pass

    async def prepare(self):
        """
        
        before real handler runs
        
        1. update request id
        
        :return: 
        """
        request_id = self.request.headers.get("X-Request-ID")
        if request_id:
            RequestIDContext._data.request_id = request_id
        else:
            self.set_header("X-Request-ID", RequestIDContext._data.request_id)

    def json(self, error, data):
        self.write(Response.build_output(error, data))

    def _set_header(self):
        """
        设置response header
        
        :return:
        """
        self.set_header("Content-Type", "text/javascript;charset=UTF-8")
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.set_header("Expires", "0")
        self.set_header("Pragma", "no-cache")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, PATCH, DELETE, HEAD, OPTIONS")
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin", ""))

    def _set_ssl(self):
        """
        设置协议 http 或者 https
        
        :return:
        """
        if self.request.headers.get("Ssl") == "on":
            self.https = True
            self.scheme = "https://"
        else:
            self.https = False
            self.scheme = "http://"
