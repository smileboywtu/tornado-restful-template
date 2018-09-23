# -*- coding: utf-8 -*-

"""

application define

:create: 2018/9/23
:copyright: smileboywtu

"""

from tornado.web import Application

from application.router import routers
from common.loggers import log_function


def make_app(cookie_secret):
    app = Application(
        handlers=routers,
        cookie_secret=cookie_secret,
        log_function=log_function
    )
    return app
