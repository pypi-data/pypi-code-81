# -*- coding: utf-8 -*-
# Author: Eamonn
# Email: china.eamonn@gmail.com
# Link: https://elanpy.com

import aiohttp
import chardet
import asyncio
import fuclib
import parsel
from urllib.parse import urljoin
from yarl import URL
from w3lib.encoding import (html_to_unicode, http_content_type_encoding)
import json as js

import logging
from logging import error

logger = logging.getLogger(__name__)


def random_ua():
    """
    随机浏览器头
    :return:
    """
    import random
    user_agent_list = [
        'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language} rv:{Firefox}) Gecko/{builddata} Firefox/{Firefox}'.format(
            **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10.0"]),
               'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
               'language': random.choice(["", " {};".format("zh-CN")]), 'builddata': random.choice(
                    ["201{}0{}{}".format(random.randint(0, 6), random.randint(1, 9), random.randint(10, 28))]),
               'Firefox': random.choice(
                   ["50.0.1", "50.0.2", "50.0", "50.01", "50.010", "50.011", "50.02", "50.03", "50.04", "50.05",
                    "50.06", "50.07", "50.08", "50.09", "50.1.0", "51.0.1", "51.0", "51.01", "51.010", "51.011",
                    "51.012", "51.013", "51.014", "51.02", "51.03", "51.04", "51.05", "51.06", "51.07", "51.08",
                    "51.09", "52.0.1", "52.0.2", "52.0", "52.01", "52.02", "52.03", "52.04", "52.05", "52.06",
                    "52.07", "52.08", "52.09", "52.1.0", "52.1.1", "52.1.2", "52.2.0", "52.2.1", "52.3.0", "52.4.0",
                    "52.4.1", "53.0.2", "53.0.3", "53.0", "53.01", "53.010", "53.02", "53.03", "53.04", "53.05",
                    "53.06", "53.07", "53.08", "53.09", "54.0.1", "54.0", "54.01", "54.010", "54.011", "54.012",
                    "54.013", "54.02", "54.03", "54.04", "54.05", "54.06", "54.07", "54.08", "54.09", "55.0.1",
                    "55.0.2", "55.0.3", "55.0", "55.01", "55.010", "55.011", "55.012", "55.013", "55.02", "55.03",
                    "55.04", "55.05", "55.06", "55.07", "55.08", "55.09", "56.0.1", "56.0", "56.01", "56.010",
                    "56.011", "56.012", "56.02", "56.03", "56.04", "56.05", "56.06", "56.07", "56.08", "56.09",
                    "57.03", "57.04", "57.05", "57.06"]), }),
        'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language}) AppleWebKit/{Safari} (KHTML, '
        'like Gecko) Chrome/{Chrome} Safari/{Safari}'.format(
            **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
               'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
               'language': random.choice(["", " {};".format("zh-CN")]),
               'Chrome': '{0}.{1}.{2}.{3}'.format(random.randint(50, 61), random.randint(0, 9),
                                                  random.randint(1000, 9999), random.randint(10, 99)),
               'Safari': '{0}.{1}'.format(random.randint(100, 999), random.randint(0, 99)), }),
        'Mozilla/5.0 ({compatible}Windows NT {WindowsNT};{WOW64} MSIE {ie}.0; Trident/{Trident}.0;){Gecko}'.format(
            **{'compatible': random.choice(["", "compatible; "]),
               'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
               'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
               'ie': random.randint(10, 11), 'Trident': random.randint(5, 7),
               'Gecko': random.choice(["", " like Gecko;"])}),
        'Mozilla/5.0 (Windows NT {WindowsNT}; MSIE 9.0;) Opera {opera1}.{opera2}'.format(
            **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
               'opera1': random.randint(10, 12), 'opera2': random.randint(10, 99)}),
    ]
    rs = random.choice(user_agent_list)  # 201706  firefox14 chrome63 ie9 opera2
    return rs


class Response:
    def __init__(self, data, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, meta=None, res=None):
        if meta is None:
            meta = {}
        self.url = str(res.url)
        self.data = data
        self.body = self.content = content
        self.status = self.status_code = status_code
        self.charset = charset
        self.res = res
        self.cookies = {k: v.value for k, v in self.res.cookies.items()}
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.meta = meta if meta else {}
        self.__r = parsel.Selector(self.text)

    def __str__(self):
        return self.text

    @property
    def text(self):
        if not self.content:
            return ''
        if self.charset:
            try:
                text = self.content.decode(self.charset)
            except UnicodeDecodeError:
                try:
                    benc = http_content_type_encoding(dict(self.res.headers)['Content-Type'])
                    if benc:
                        charset = 'charset=%s' % benc
                        text = html_to_unicode(charset, self.body)[1]
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        char = chardet.detect(self.content)
                        if char:
                            text = self.content.decode(char['encoding'])
                        else:
                            raise UnicodeDecodeError
                    except UnicodeDecodeError:
                        try:
                            text = self.content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                text = self.content.decode("gb18030")
                            except UnicodeDecodeError:
                                text = self.content.decode('utf-8', "ignore")
        else:
            try:
                text = self.content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(self.content)
                    if char:
                        text = self.content.decode(char['encoding'])
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = self.content.decode('gb18030')
                    except UnicodeDecodeError:
                        text = self.content.decode('utf-8', "ignore")
        return text

    @property
    def json(self):
        return js.loads(self.text, strict=False)

    def xpath(self, x):
        return self.__r.xpath(x)

    def css(self, x):
        return self.__r.css(x)

    def urljoin(self, url):
        return urljoin(self.url, url)


class Retry(object):
    def __init__(self, max_times=3):
        self.func = None
        self.max_times = max_times

    async def run(self, session, request):
        retry_times = 0
        while retry_times < self.max_times:
            try:
                return await self.func(session, request)
            except TimeoutError:
                error(f"第{retry_times + 1}次请求超时，url：{request['url']}")
                retry_times += 1
            except Exception as e:
                error(f"第 {retry_times + 1} 次请求报错({type(e).__name__}: {e})，url：{request['url']}")
                retry_times += 1

    def __call__(self, func):
        self.func = func
        return self.run


class Request:
    @staticmethod
    @Retry()
    async def quest(session, request):
        if request['method'].upper() == 'GET':
            async with session.get(URL(request['url'], encoded=request.get('url_encoded', False)),
                                   params=request.get('params', None), cookies=request.get('cookies', None),
                                   headers=request.get('headers', None), proxy=request.get('proxies', None),
                                   allow_redirects=request.get('allow_redirects', True),
                                   timeout=request.get('time_out', 180),
                                   proxy_auth=aiohttp.BasicAuth(fuclib.proxyUser, fuclib.proxyPass)) as res:
                text = await res.read()

        elif request['method'].upper() == 'POST':
            async with session.post(URL(request['url'], encoded=request.get('url_encoded', False)),
                                    data=request.get('data', None), json=request.get('json', None),
                                    cookies=request.get('cookies', None), headers=request.get('headers', None),
                                    proxy=request.get('proxies', None),
                                    allow_redirects=request.get('allow_redirects', True),
                                    timeout=request.get('time_out', 180),
                                    proxy_auth=aiohttp.BasicAuth(fuclib.proxyUser, fuclib.proxyPass)) as res:
                text = await res.read()
        else:
            raise "{%s}请求方式未定义，请自定义添加！" % request['method']

        if res:
            status_code = res.status
            charset = res.charset
            response = Response(request.get('data'), text, status_code, charset, request.get('cookies', None),
                                request['method'], request.get('headers', None), request.get('callback', "parse"),
                                request.get('proxies', None), request.get('meta', None), res)
            return response

    @staticmethod
    async def new_session(verify=False):
        connector = aiohttp.TCPConnector(ssl=verify)
        session = aiohttp.ClientSession(connector=connector, trust_env=True)
        return session

    @staticmethod
    async def get(session, request):
        async with session.get(request['url'], params=request['params'], cookies=request['cookies'],
                               headers=request['headers'], proxy=request['proxies'],
                               allow_redirects=request['allow_redirects'], timeout=request.get('time_out', 180)) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def post(session, request):
        async with session.post(request['url'], data=request['data'], json=request['json'], cookies=request['cookies'],
                                headers=request['headers'], proxy=request['proxies'],
                                allow_redirects=request['allow_redirects']) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def exit(session):
        await session.close()

    @staticmethod
    def func(future):
        logger.info(future.result())
        return future.result()
