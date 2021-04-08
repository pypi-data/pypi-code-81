class BusinessInterruptException(Exception):
    """业务中断异常，不再执行后面逻辑"""

    def __init__(self, status, msg):
        Exception.__init__(self)
        self.status = status
        self.msg = msg

    def __str__(self):
        return 'status:{},msg:{}'.format(self.status, self.msg)


class GracefulExitException(Exception):
    """终止退出抛出的异常"""

    def __init__(self, data=None):
        Exception.__init__(self)
        self.data = data
