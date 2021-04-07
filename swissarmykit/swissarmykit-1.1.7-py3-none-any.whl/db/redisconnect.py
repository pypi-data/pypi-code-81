import redis
from swissarmykit.lib.core import Singleton
from swissarmykit.conf import *


class RedisUtils:

    def __init__(self, config='redis'):
        self.redis = redis.Redis(**swissarmykit_conf.config.get(config))

    def get_restrict(self, config='redis'):
        return redis.StrictRedis(**swissarmykit_conf.config.get(config))

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, ex=3600):
        self.redis.set(key, value, ex=ex)

    def delete(self, key):
        self.redis.delete(key)

    def delete_namespace(self, ns):
       prefix = '%s:*' % ns
       for key in self.redis.scan_iter(prefix):
           self.delete(key)

    def lpush(self, name, value):
        self.redis.lpush(name, value)

    def get_list(self, name):
        return self.redis.lrange(name, 0, -1)


    def add_set(self, name, value):
        ''' add Value into SET '''
        return self.redis.sadd(name, value)

    def get_set(self, name, to_string=False, to_int=False):
        if to_string:
            return {i.decode() for i in self.redis.smembers(name)}

        if to_int:
            return {int(i) for i in self.redis.smembers(name)}

        return self.redis.smembers(name)


@Singleton
class RedisConnect(RedisUtils):

    def __init__(self, config='redis'):
        try:
            self.redis = redis.Redis(**swissarmykit_conf.config.get(config))
        except Exception as e:
            self.log.error(e)
            exit()
            super().__init__(config)

@Singleton
class OtherRedisConnect(RedisUtils):

    def __init__(self, config='redis'):
        try:
            self.redis = redis.Redis(**swissarmykit_conf.config.get('other_db').get(config))
        except Exception as e:
            self.log.error(e)
            exit()
            super().__init__()

if __name__ == '__main__':
    o = RedisConnect.instance()
    o.add_set('test', '1')

    print(set(o.get_set('test')))