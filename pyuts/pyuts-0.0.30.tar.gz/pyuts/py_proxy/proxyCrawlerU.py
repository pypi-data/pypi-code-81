# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ProxyCrawlerU(PyApiB):
    """
    代理相关工具
    """
    
    crawlerEnable = True
    """ 如果爬虫暂时不启用，将此设为False即可 """
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def getProxys(self) -> list:
        """ 获取和解析代理
        {"host":"xx.xx.xx.xx","port":"xxxx","user":"","pswd":"","perSec":"","sourceName":"","header":"xxx:xxx;zzz:xxx;"}
        """
        return []
    
    