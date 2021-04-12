import logging
from logging import Logger
import os


# 获取日志对象
def get_logger(directory: str = '.', filename: str = 'logger.log', encoding: str = 'utf-8',
               mode: str = 'a',
               fmt: str = '%(asctime)s %(levelname)s %(message)s',
               datefmt: str = '%m/%d/%Y %H:%M:%S', use_stream: bool = False) -> Logger:
    """
    生成日志对象
    记录消息：日志对象.info('xxx')即可
    例子：
    import elogger
    logger = elogger.get_logger()
    logger.info('hello world!')
    Args:
        directory: 日志存放的目录
        filename: 日志文件的存放路径
        encoding: 日志记录编码格式
        mode: 日志写入格式
        fmt: 日志格式，写法与logging的fmt参数相同
        datefmt: 时间格式，写法与logging的datefmt参数相同
        use_stream: 是否在终端打印日志，True表示是，False表示否

    Returns:
        e_logger: 日志对象 Logger
    """
    path = os.path.join(directory, filename)
    e_logger = logging.getLogger()
    if not os.path.exists(directory):
        os.mkdir(directory)
        open(filename, mode='w', encoding='utf-8')
    fh = logging.FileHandler(filename=path, encoding=encoding, mode=mode)
    f = logging.Formatter(fmt=fmt, datefmt=datefmt)
    fh.setFormatter(f)
    e_logger.setLevel(logging.INFO)
    if use_stream:
        ph = logging.StreamHandler()
        ph.setFormatter(f)
        e_logger.addHandler(ph)
    e_logger.addHandler(fh)
    return e_logger


if __name__ == '__main__':
    get_logger()
