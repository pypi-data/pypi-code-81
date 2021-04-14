import typing as T
from pydantic import BaseModel, PrivateAttr
from magicdb.utils.Redis.decorators import decorate_redis
import redis


class RedisModel(BaseModel):
    host: str
    port: int
    password: str
    decode_responses: bool = True
    ttl_secs: int = None
    error_thrower: T.Callable = None
    use_redis_span: bool = True

    _r: T.Optional[redis.Redis] = PrivateAttr(None)

    @property
    def r(self) -> T.Optional[redis.Redis]:
        if not self._r:
            self._r = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=self.decode_responses,
            )
            if self.use_redis_span:
                decorate_redis(r=self._r, error_thrower=self.error_thrower)
        return self._r

    def refresh(self) -> T.Optional[redis.Redis]:
        self._r = None
        return self.r
