from datetime import datetime
from http import HTTPStatus
import uuid
import os


def get_http_status_mapping():
    # Enum has a member called _value2member_map_
    # ( which is undocumented and may be changed/removed in future python versions)
    res = getattr(HTTPStatus, "_value2member_map_", None)
    if res is None:
        res = dict((m.value, m) for m in HTTPStatus)
    return res


_env = os.environ.setdefault
HTTP_STATUS_ENUMS_MAP = get_http_status_mapping()


class JsonResponse():
    DEFAULT_VERSION = int(_env("HTTP_JSON_API_VERSION", "2"))
    DEFAULT_ERRNO = int(_env("HTTP_JSON_API_ERRNO", "40000"))

    @staticmethod
    def describe_status(code):
        status_enum = HTTP_STATUS_ENUMS_MAP.get(code, None)
        if status_enum is not None:
            return f"[{status_enum.name}:{code}] {status_enum.description}"
        return f"[???:{code}] invalid http status !!!"

    @classmethod
    def format(cls, err: Exception):
        if not isinstance(err, BaseApiError):
            err = BaseApiError(
                msg=getattr(err, "msg", str(err)),
                errno=getattr(err, "errno", cls.DEFAULT_ERRNO),
                tracked_error=err,
            )
        cal = getattr(cls, f"format_v{cls.DEFAULT_VERSION}")
        if not callable(cal):
            cal = cls.format_v2
        return cal(err)

    @staticmethod
    def format_v0(err):
        # version:0
        # response200: {result=$, errno=0}
        return dict(
            errno=err.errno,
            msg=err.msg,
        )

    @staticmethod
    def format_v1(err):
        # version:1
        # response200: {success=True, result=$}
        return dict(
            errno=err.errno,
            success=False,
            message=err.msg,
        )

    @staticmethod
    def format_v2(err):
        # version: 2
        # response200: {code=0, result=$, <request_id>, <error>}
        m = dict(
            code=err.errno,  # type: int
            error=f"[{err.__class__.__name__}] {err.msg}",  # type: str
            request_id=err.request_id,
        )
        if err.kwargs:
            m["error_info"] = err.kwargs
        return m

    @staticmethod
    def format_v3(err):
        # version: 3
        # response200:  {result=$, <request_id>}
        return dict(
            errno=err.errno,
            error_msg=err.msg,
            error_info=err.kwargs,
            error_name=err.__class__.__name__,
            request_id=err.request_id,
        )


class BaseApiError(Exception):
    errno = 40000  # customize 5-digit-number, status_code * 100
    status = 400
    msg = ""

    def __init__(self, msg="", **kwargs):
        super().__init__()
        self.errno = kwargs.pop("errno", self.errno)
        self._request_id = kwargs.pop("request_id", None)
        status = kwargs.get("status", self.errno // 100)  # http status code, return type: int
        self._set_status(status)
        self.kwargs = kwargs
        self.msg = msg or self.msg

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        description = f"[{self.__class__.__name__}:{self.errno}:{self.request_id}] {self.msg}"
        return f"{description} => ({self.status_msg}:{self.status})"

    def _set_status(self, status: int):
        status_enum = HTTP_STATUS_ENUMS_MAP.get(status)
        if not status_enum:
            self.status_msg = ""
        else:
            self.status = status
            self.status_msg = status_enum.name

    @staticmethod
    def new_request_id(prefix="x"):
        ct = datetime.now().strftime("%m%d%H%M%S")
        rnd = str(uuid.uuid4())[:4]
        return ''.join([prefix, ct, "_", rnd])

    @property
    def request_id(self):
        if not self._request_id:
            self._request_id = self.new_request_id()
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value

    def to_dict(self, **kwargs):
        data = JsonResponse.format(self)  # type: dict
        for k, v in kwargs.items():
            if v is not None:
                data[k] = v
            else:
                data.pop(k, v)
        return data
