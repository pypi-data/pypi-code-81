import os.path
import logging
from logging import handlers


class Logger():
    """
    定义一个专门处理日志的类，供其他模块调用
    """

    # 定义日志级别的映射关系
    level_rel = {"DEBUG": logging.DEBUG,
                 "INFO": logging.INFO,
                 "WARNING": logging.WARNING,
                 "ERROR": logging.ERROR,
                 "CRITICAL": logging.CRITICAL
                 }

    def __init__(self, file_name="run.log",
                 fmt="%(asctime)s - %(module)s[line:%(lineno)d] - %(levelname)s: %(message)s",
                 when="D", back_count=3):
        # 创建一个logger
        self.logger = logging.getLogger(file_name)

        # 获取配置文件中的日志级别，转换成大写
        # level = Util().get_config("logLevel", "level").upper()
        level = "INFO"
        # 设置日志级别
        self.logger.setLevel(self.level_rel.get(level))
        # 创建日志格式
        format = logging.Formatter(fmt)
        if not self.logger.handlers:
            # 创建一个输出到控制台的handler
            sh = logging.StreamHandler()
            sh.setFormatter(format)
            # 把handler对象添加到logger
            self.logger.addHandler(sh)

            # 定义log名称，os.path.realpath(__file__)获取绝对路径，通过两层的os.path.dirname，获取到项目根目录

            # log_name = os.path.dirname(os.path.realpath(__file__)) + "/logs/" + file_name

            # log_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/logs/" + file_name
            # 创建一个输出到文件的handler
            # fh = handlers.TimedRotatingFileHandler(filename=log_name, when=when, backupCount=back_count,
            #                                        encoding="utf-8")
            # fh.setFormatter(format)
            # self.logger.addHandler(fh)

    def get_logger(self):
        """
        返回日志类的实例
        """
        return self.logger

logger = Logger().get_logger()
