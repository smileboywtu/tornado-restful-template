# -*- coding: utf-8 -*-


from motor import motor_tornado
from pymongo import ReadPreference
from pymongo.errors import InvalidName


class MongoTK():
    __slots__ = ["__client", "__database", "__collection"]

    def __init__(self):
        if not hasattr(MongoTK, "connection_pool"):
            raise EnvironmentError("should call MongoTK.initialize_pool before using instance")
        self.__client = MongoTK.connection_pool
        self.__database = None
        self.__collection = None

    @property
    def pool(self):
        return self.__client

    @property
    def collection(self):
        if not self.__collection or not self.__database:
            raise ValueError("must build database and collection firstly")
        try:
            return self.__client[self.__database][self.__collection].with_options(
                read_preference=ReadPreference.SECONDARY_PREFERRED)
        except InvalidName:
            self.__client[self.__database].create_collection(self.collection)
            return self.__client[self.__database][self.__collection].with_options(
                read_preference=ReadPreference.SECONDARY_PREFERRED)

    def build_database(self, database):
        self.__database = database
        return self

    def build_collection(self, collection):
        if not self.__database:
            raise ValueError("build database first")
        self.__collection = collection
        return self

    @staticmethod
    def initialize_pool(*args, **kwargs):
        """
        创建 mongo 连接， 连接参数参照 pymongo

        min_connections: 5
        max_connections: 20

        :param args:
        :param kwargs:
        :return:
        """
        MongoTK.connection_pool = motor_tornado.MotorClient(
            *args,
            # maxPoolSize=1,
            # minPoolSize=5,
            # socketTimeoutMS=2000,
            connectTimeoutMS=1000,
            retryWrites=True,
            appname="GCloud",
            **kwargs)
