# -*- coding: utf-8 -*-

"""


:create: 2018/9/23
:copyright: smileboywtu

"""
from application.handlers.counter.handler import CounterView

routers = [
    ("/api/v1/counter", CounterView),

]
