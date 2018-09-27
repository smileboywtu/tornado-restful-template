# -*- coding: utf-8 -*-


"""

celery 初始化

:create: 2018/9/23
:copyright: smileboywtu

"""

from celery import Celery

from run import load_settings

settings = load_settings("config.yaml").settings


redis_url = "redis://:{0}@{1}:{2}/{3}".format(
    settings["REDIS_PASSWD"],
    settings["REDIS_HOST"],
    settings["REDIS_PORT"],
    settings["REDIS_DB"]
)

celery_app = Celery(
    broker=redis_url,
    backend=redis_url,
)

## more config
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

## found celery_tasks
celery_app.autodiscover_tasks([
    "celery_tasks",
], force=True)


## 添加定时任务
celery_app.conf.beat_schedule = {
    "parse_log": {
        "task": "parse_log",
        "schedule": 30
    }
}