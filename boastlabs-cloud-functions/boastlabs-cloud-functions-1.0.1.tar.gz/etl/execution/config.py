API_VERSION = "1.0.0"

TIMEOUT_SECONDS = 360


class Status:
    NEW = 'new'
    RUNNING = 'running'
    FAILED = 'failed'
    DONE = 'done'
    SLEEP = 'sleep'

    WAITING_RETRY = 'waiting_retry'
    WAITING_SLEEP = 'waiting_sleep'
