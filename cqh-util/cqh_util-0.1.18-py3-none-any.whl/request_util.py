from .escape_util import escape_unicode_escape
import logging

_logger = logging.getLogger(__name__)


async def request_tornado_repeat_request(request_fuc, retry_code_range_list=((599, 600)), max_request_count=5,
                                         logger=_logger,
                                         fail_message=''):
    from tornado.simple_httpclient import HTTPError
    # 为了安装这个包的时候，tornado不是必须的

    # 为了安装这个包的时候，tornado不是必须的
    for i in range(max_request_count):
        res = await request_fuc()
        # generated_by_dict_unpack: res
        code, body = res.code, res.body
        body = body or b''
        body = escape_unicode_escape(body)
        logger.info("res: code:{}, body:{}, cost:{}".format(code, body, res.request_time))

        is_match = False
        for code_range in retry_code_range_list:
            # logger.info("code_range:{}".format(code_range))
            if code >= code_range[0] and code < code_range[1]:
                is_match = True
                break
        if is_match:
            if i < max_request_count - 1:
                continue
            else:
                raise HTTPError(res.code, message=fail_message)
        else:
            return res


def request_requests_reapeat_request(request_func, max_request_count=5, timeout=(5, 20)):
    from requests.exceptions import ConnectionError, ReadTimeout
    for i in range(max_request_count):
        try:
            res = request_func()
            return res
        except ConnectionError:
            if i < max_request_count - 1:
                continue
            else:
                raise
        except ReadTimeout:
            if i < max_request_count - 1:
                continue
            else:
                raise


def request_simple_unpack_tornado_res(res):
    # generated_by_dict_unpack: res
    code, body = res.code, res.body
    body = escape_unicode_escape(body or b'')
    return code, body


def request_logger_tornado_res(logger, res, method='info'):
    code, body = request_simple_unpack_tornado_res(res)
    getattr(logger, method)('code:{}, body:{}, cost:{}'.format(code, body, res.request_time))
