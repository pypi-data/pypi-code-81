# -*- coding: UTF-8 -*-
import json
import tornado.web
import inspect
from ..py_api_b import PyApiB
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor


class HttpHandlerU(tornado.web.RequestHandler, PyApiB):
    """
    HTTP服务器端接口基类
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    executor = ThreadPoolExecutor(64) # 并发数

    getPath: str = None
    """ 
    复写get方法时需要给getPath付值，如：/test 
    """
    postPath: str = None
    """ 复写post方法时需要给postPath付值，如：/test """
    connectPath: str = None
    """ 复写connect方法时需要给connectPath付值，如：/test """
    
    @gen.coroutine
    def get(self, *args, **kwargs):
        res = self.syncGet(*args, **kwargs)
        if res == None:
            res = {}
        self.returnData(data=res.get("data"),code=res.get("code",200),msg=res.get("msg"))

    @gen.coroutine
    def post(self, *args, **kwargs):
        res = self.syncPost(*args, **kwargs)
        if res == None:
            res = {}
        self.returnData(data=res.get("data","{}"),code=res.get("code",200),msg=res.get("msg",""))
       
    @run_on_executor 
    def syncGet(self, *args, **kwargs):
        return {"data":None, "code":200, "msg":"OK"}
    
    @run_on_executor
    def syncPost(self, *args, **kwargs):
        return {"data":None, "code":200, "msg":"OK"}
    
    def getHttpServerU(self):
        return getattr(self, "httpServerU")

    def returnData(self, data=None, code=200, msg='OK'):
        """
        返回数据
        
        Args:

        """
        self.write(
            json.dumps({
                'code': code,
                'msg': msg,
                'data': {} if data == None else data
            }))
        self.finish()