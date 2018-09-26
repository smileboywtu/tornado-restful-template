# -*- coding: utf-8 -*-

"""

定期健康检查，并上报到redis中，或者短信通知
其余部分可以自行扩展

:create: 2018/9/23
:copyright: smileboywtu

"""

async def health_check():
    print("--> ")