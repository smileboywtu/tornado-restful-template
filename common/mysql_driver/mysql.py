# -*- coding: utf-8 -*-

"""


:create: 2018/9/23
:copyright: smileboywtu

"""


from aiomysql import create_pool



class MysqlTK():
    __slots__ = ["__client"]

    def __init__(self):
        if not hasattr(MysqlTK, "connection_pool"):
            raise EnvironmentError("should call MysqlTK.initialize_pool before using instance")
        self.__client = MysqlTK.connection_pool

    @property
    def pool(self):
        return self.__client

    @property
    def connection(self):
        return self.__client.get()

    @staticmethod
    async def initialize_pool(*args, **kwargs):
        """
        创建 mysql 连接， 连接参数参照 pymysql

        min_connections: 5
        max_connections: 20

        :param args:
        :param kwargs:
        :return:
        """
        MysqlTK.connection_pool = await create_pool(*args, **kwargs)

    async def execute(self, sql, params=None):
        """
        测试 执行
        :return:
        """
        async with self.connection as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, params)
                return await cursor.fetchall()