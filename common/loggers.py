# -*- coding: utf-8 -*-

"""
配置日志信息，并添加 request_id

:create: 2018/9/23
:copyright: smileboywtu

"""
import datetime
import logging
import uuid
from logging.handlers import RotatingFileHandler

from tornado import gen
from tornado.log import access_log
from tornado.stack_context import run_with_stack_context, StackContext


class RequestIDContext:
    class Data:
        def __init__(self, request_id=0):
            self.request_id = request_id

        def __eq__(self, other):
            return self.request_id == other.request_id

    _data = Data()

    def __init__(self, request_id):
        self.current_data = RequestIDContext.Data(request_id=request_id)
        self.old_data = None

    def __enter__(self):
        if RequestIDContext._data == self.current_data:
            return

        self.old_context_data = RequestIDContext.Data(
            request_id=RequestIDContext._data.request_id,
        )

        RequestIDContext._data = self.current_data

    def __exit__(self, exc_type, exc_value, traceback):
        if self.old_data is not None:
            RequestIDContext._data = self.old_data


def with_request_id(func):
    @gen.coroutine
    def _wrapper(*args, **kwargs):
        request_id = uuid.uuid4().hex
        yield run_with_stack_context(StackContext(lambda: RequestIDContext(request_id)), lambda: func(*args, **kwargs))

    return _wrapper


def log_function(handler):
    """
    log function to log access request information

    regex parse: (?<remote_ip>[\d.]+) [-\w]+ [-\w]+ \[(?<request_date>[\d\/:\s\+]+)\] \"
    (?<http_method>[A-Z]+) (?<http_uri>[\/a-zA-Z\.]+) (?<http_version>[A-Z\/\d\.]+)\"
    (?<status_code>[\d]+) (?<length>[\d]+)
    (?<request_time>[\d\.]+) (?<request_id>[\d\w]+) [\w\-]+ \[(?<request_body>.+)\] -

    :param handler:
    :return:
    """

    _log_meta = dict(
        app_id="app-up",
        user="-",
        username="-",
        response_code="-",

        http_uri=handler.request.uri,
        http_status=handler.get_status(),
        http_method=handler.request.method,
        http_version=handler.request.version,

        remote_ip=handler.request.remote_ip,
        request_time=1000.0 * handler.request.request_time(),
        request_id=RequestIDContext._data.request_id,

        response_length=handler.request.headers.get("Content-Length", 0),
        request_args=handler.request.arguments,
        request_date=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%x:%H:%M:%S %z")
    )

    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error

    log_method("%(remote_ip)s %(user)s %(username)s [%(request_date)s] \"%"
               "(http_method)s %(http_uri)s %(http_version)s\" %(http_status)s "
               "%(response_length)s %(request_time).2f %(request_id)s %(app_id)s [%(request_args)s] -", _log_meta)


def logger_config(name, path, level, log_format, max_bytes, backup_count):
    """
     配置 log handler 对象
     
    :param name: 日志名称
    :param path: 日志文件路径
    :param level: 日志等级
    :param log_format: 日志格式
    :param max_bytes: 日志文件最大大小
    :param backup_count: 日志文件滚动个数
    :return:
    """
    handler = RotatingFileHandler(path, "a", maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)


def configure_tornado_logger(path, name="tornado.application"):
    """
    
    ## read doc:
    https://docs.python.org/3/library/logging.html#logrecord-attributes
    
    tornado web application log_format:
    %(asctime)s %(levelname)s %(request_id)-%(process)d %(filename)s:%(lineno)d -- %(message)s
    
    :param path: log file path
    :param name: log name
    :return: 
    """
    if name == "tornado.access":
        log_format = "%(message)s"
    else:
        log_format = "%(asctime)s %(levelname)s %(request_id)s-%(process)d %(filename)s:%(lineno)d -- %(message)s"

    return logger_config(
        name=name,
        path=path,
        level="DEBUG",
        log_format=log_format,
        max_bytes=100 * 1024 * 1024,
        backup_count=7
    )
