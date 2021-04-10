from JCoder_redis import Redis


class Ordered_set(Redis):

    def __init__(self, host: str = 'localhost', port: int = 6379, default_db: int = 0, is_decode: bool = True):
        """

        :param host:
        :param port:
        :param default_db:
        :param is_decode:
        """
        super().__init__(host, port, default_db, is_decode)

    def __setitem__(self, key: str, value):
        """

        :param key:
        :param value:
        :return:
        """
        super().delete(key)
        for i in (value[0] if type(value)==tuple else value):
            self._redis.zadd(key, i)
        if type(value)==tuple:
            super().expire(key,value[1])

    def __iadd__(self, other:tuple):
        """

        :param other:
        :return:
        """
        for i in other[1]:
            self._redis.zadd(other[0],i)

    def length(self,key:str) -> int :
        """

        :param key:
        :return:
        """
        return self._redis.zcard(key)

    def __getitem__(self, item:tuple):
        """

        :param item:
        :return:
        """
        return self._redis.zrange(item[0],0,-1,withscores=item[1])

    def get_range(self,name:str,start:int=0,end:int=-1,desc:bool=False,withscores:bool=False,score_cast_func=float):
        """

        :param name:
        :param start:
        :param end:
        :param desc:
        :param withscores:
        :param score_cast_func:
        :return:
        """
        return self._redis.zrange(name=name,start=start,end=end,desc=desc,withscores=withscores,score_cast_func=score_cast_func)

    def get_range_by_score(self,name:str,min,max,start:int=None,num:int=None,desc:bool=False,withscores:bool=False,score_cast_func=float):
        """

        :param name:
        :param min:
        :param max:
        :param start:
        :param num:
        :param desc:
        :param withscores:
        :param score_cast_func:
        :return:
        """
        if desc:
            return self._redis.zrangebyscore(name=name,min=min,max=max,start=start,num=num,withscores=withscores,score_cast_func=score_cast_func)
        return self._redis.zrevrangebyscore(name=name,min=min,max=max,start=start,num=num,withscores=withscores,score_cast_func=score_cast_func)

    def get_range_by_lex(self,name:str,min,max,start:int=None,num:int=None,desc:bool=False,withscores:bool=False):
        """

        :param name:
        :param min:
        :param max:
        :param start:
        :param num:
        :param desc:
        :param withscores:
        :param score_cast_func:
        :return:
        """
        if desc:
            return self._redis.zrangebylex(name=name,min=min,max=max,start=start,num=num,withscores=withscores)
        return self._redis.zrevrangebylex(name=name,min=min,max=max,start=start,num=num,withscores=withscores)

    def scan(self,name:str,cursor:int=0,match=None,count=None,score_cast_func=float):
        """
        获取元素--默认按照分数顺序排序
        :param name:
        :param cursor:
        :param match:
        :param count:
        :param score_cast_func:
        :return:
        """
        return self._redis.zscan(name=name,cursor=cursor,match=match,count=count,score_cast_func=score_cast_func)

    def ergodic(self,name:str,match=None,count=None,score_cast_func=float):
        """

        :param name:
        :param match:
        :param count:
        :param score_cast_func:
        :return:
        """
        return self._redis.zscan_iter(name=name,match=match,count=count,score_cast_func=score_cast_func)

    def count(self,name:str,min,max) -> int:
        """
        获取name对应的有序集合中分数 在 [min,max] 之间的个数
        :param min:
        :param max:
        :return:
        """
        return self._redis.zcount(name=name,min=min,max=max)

    def increase(self,name:str,key:str,amount):
        """

        :param name:
        :param key:
        :param amount:
        :return:
        """
        self._redis.zincrby(name=name,amount=amount,value=key)

    def get_rank(self,name:str,key) -> int:
        """

        :param name:
        :param key:
        :return:
        """
        return self._redis.zrank(name,key)

    def get_score(self,name:str,key):
        """

        :param name:
        :param key:
        :return:
        """
        return self._redis.zscore(name,key)

    def del_by_score(self,name:str,min,max):
        """

        :param name:
        :param min:
        :param max:
        :return:
        """
        self._redis.zremrangebyscore(name=name,min=min,max=max)

    def del_by_rank(self,name:str,min:int,max:int):
        """

        :param name:
        :param min:
        :param max:
        :return:
        """
        self._redis.zremrangebyrank(name=name,min=min,max=max)

    def del_by_lex(self,name:str,min,max):
        """

        :param name:
        :param min:
        :param max:
        :return:
        """
        self._redis.zremrangebylex(name=name,min=min,max=max)

    def remove(self,name:str,*key):
        """

        :param name:
        :param key:
        :return:
        """
        self._redis.zrem(name=name,*key)