from .. import *  # NOQA

CELERY_TASK_ALWAYS_EAGER = False
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
