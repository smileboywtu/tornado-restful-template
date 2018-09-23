# -*- coding: utf-8 -*-

"""

入口程序

:create: 2018/9/23
:copyright: smileboywtu

"""

import asyncio
import os

from tornado.httpserver import HTTPServer
from tornado.process import task_id

from application.app import make_app
from application.health_check import health_check
from common.loggers import configure_tornado_logger
from common.mysql_driver import MysqlTK
from common.redis_driver import RedisTK


async def init_db():
    """
    初始化数据库连接
    :return:
    """
    # await RedisTK.initialize_pool()
    # await MysqlTK.initialize_pool()


def before_fork_init(app):
    """

    在 fork 之前，执行的任务, 主要加载全局的资源
    这部分资源会在 fork 时候从主进程拷贝到各个子进程

    :param app:
    :return:
    """

    project_root = os.path.dirname(__file__)
    app.settings["project_root"] = project_root

    # 加载国际化文件
    # 加载其他全局共享只读内容


def after_fork_init(ioloop, app):
    """

    如果多线程模式， 那么 redis 和 mysql 的连接池创建
    应该是在 多线程 fork 之后, 保证不通的 python interpreter
    拥有独立的资源

    :param ioloop:
    :param app:
    :return:
    """

    ## 初始化连接
    ioloop.run_until_complete(init_db())

    # task ID 可以认为是 tornado 进程编号
    t_id = task_id()
    t_id = t_id if t_id else 0

    # 初始化 web 记录日志
    configure_tornado_logger(app.settings["ACC_LOG_PATH"], name="tornado.access")
    configure_tornado_logger(app.settings["APP_LOG_PATH"], name="tornado.application")
    configure_tornado_logger(app.settings["GEN_LOG_PATH"], name="tornado.general")


    # 这里保证缓存只在一个进程中进行，如果不是 multiple fork 模式的话，
    # 0 号进程负责缓存任务， 如果是多进程模式， 那么还是由编号 0 的进程
    # 任务执行缓存任务
    if t_id == 0:
        pass


async def period_health_check(ioloop, app):
    """

    进程健康检查

    :param ioloop:
    :return:
    """
    await asyncio.sleep(app.settings["HEALTH_CHECK_PERIOD"])
    await health_check()
    ioloop.create_task(period_health_check(ioloop, app))


def load_settings(config_file):
    """
    load all config setting into tornado app settings.
    
    :param config_file: config file 
    
    :return: 
    """
    return {
        "COOKIE_SECRET": "example",
        "PORT": 8009,
        "PROCESS_NUM": 1,
        "HEALTH_CHECK_PERIOD": 5,
        "APP_LOG_PATH": "app.log",
        "GEN_LOG_PATH": "gen.log",
        "ACC_LOG_PATH": "access.log"
    }


def start_server():
    """
    启动服务
    :return:
    """
    ## load settings
    settings = load_settings("config.yaml")

    ## create app and update settings
    app = make_app(settings["COOKIE_SECRET"])
    app.settings.update(settings)

    ## before fork
    before_fork_init(app)
    server = HTTPServer(app, xheaders=True)
    server.bind(app.settings["PORT"])
    server.start(app.settings["PROCESS_NUM"])

    ## after fork
    ioloop = asyncio.get_event_loop()
    after_fork_init(ioloop, app)
    ioloop.run_forever()


if __name__ == "__main__":
    start_server()
