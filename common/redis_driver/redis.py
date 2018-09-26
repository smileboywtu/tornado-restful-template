# -*- coding: utf-8 -*-

"""


:create: 2018/9/23
:copyright: smileboywtu

"""

from operator import attrgetter

import aioredis


class RedisTK():
    __slots__ = ["__client"]

    def __init__(self):
        if not hasattr(RedisTK, "connection_pool"):
            raise EnvironmentError("should call RedisTK.initialize_pool before using instance")

        self.__client = RedisTK.connection_pool

    @staticmethod
    async def initialize_pool(*args, **kwargs):
        """
        创建 redis pool
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        RedisTK.connection_pool = await aioredis.create_redis_pool(
            *args, **kwargs
        )

    def __getattr__(self, item):
        return attrgetter(item)(self.__client)
