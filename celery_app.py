# -*- coding: utf-8 -*-


"""

celery 初始化

:create: 2018/9/23
:copyright: smileboywtu

"""

from celery import Celery

celery_app = Celery(
    broker="",
    backend="",

)

## more config
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)


## 添加定时任务
celery_app.conf.beat_schedule = {
    "parse_log": {
        "task": "parse_log",
        "schedule": 60
    }
}


## found celery_tasks
celery_app.autodiscover_tasks([
    "celery_tasks.parse_logs",
], force=True)