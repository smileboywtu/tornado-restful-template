# -*- coding: utf-8 -*-

"""

User Response

:create: 2018/9/23
:copyright: smileboywtu

"""
import json
import logging
from functools import wraps, partial

from tornado import stack_context, gen
from tornado.log import app_log
from tornado.stack_context import run_with_stack_context

from application.errors import ERRORS
from common.loggers import RequestIDContext


class Response():
    @classmethod
    def build_output(cls, error="success", data={}, msg="", **kwargs):
        """
        
        :param code: business code
        :param data: user data
        :param msg: notify msg
        :return: 
        """
        user_error_msg = ERRORS.get(error, ERRORS["internal_err"])
        response = {
            "code": user_error_msg["code"],
            "data": data,
            "msg": msg,
        }
        if error != "success":
            response["error"] = user_error_msg["message"]

        return json.dumps(response)


class ServerException(Exception):
    def __init__(self, error, msg, lang="zh-cn"):
        """

        :param log: use to insert log file
        :param error_code:
        :param lang:
        """
        self.output = Response.build_output(error, msg=msg, lang=lang)

    def __str__(self):
        return self.output


def _stack_context_handle_exception(type, value, traceback, handler):
    app_logger = logging.LoggerAdapter(app_log, extra={
        "request_id": RequestIDContext._data.request_id
    })
    if isinstance(value, ServerException):
        app_logger.error("%s" % str(value), exc_info=True)
        handler.write(str(value))
    elif isinstance(value, Exception):
        app_logger.error("%s" % str(value), exc_info=True)
        handler.write(Response.build_output("internal_err", msg=str(value)))
    ## make request finish
    handler.finish()

    return True


def handle_exception(method):
    @wraps(method)
    @gen.coroutine
    def __wrapper__(*args, **kwargs):
        _stack_context_handle_exception_partial = partial(_stack_context_handle_exception, handler=args[0])
        yield run_with_stack_context(
            stack_context.ExceptionStackContext(_stack_context_handle_exception_partial, delay_warning=True),
            lambda: method(*args, **kwargs)
        )

    return __wrapper__
