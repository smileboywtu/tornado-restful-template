# -*- coding: utf-8 -*-
"""

    define task for parsing logs
    
"""
from celery.task import task


@task(name="parse_log", ignore_result=True)
def parse_logs():
    print("parse_logs starting...")
