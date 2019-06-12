# -*- coding: utf-8 -*-


COOKIE_SECRET = "3pzdHaVDHSi7gV5uEgbrh3yo5tCUuhGVtq"

PORT = 9001
PROCESS_NUM = 0
DEBUG = 0

## LRU CACHE SET
LRU_CACHE_SIZE = 1000
FUNC_CACHE_EXPIRE = 60 * 60

HEALTH_CHECK_PERIOD = 5
SHUTDOWN_MAX_WAIT_TIME = 60 * 2

APP_LOG_PATH = "/app/logs/app.log"
GEN_LOG_PATH = "/app/logs/gen.log"
ACC_LOG_PATH = "/app/logs/access.log"
LOG_BACKUP = 7
LOG_ROTATE_DAY = 7
