# -*- coding: utf-8 -*-

import functools
import requests
import ujson
import re

from .logger import get_mylogger
from .utils import base64Img_encode

logger = get_mylogger('Request')


def req_logger(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                return True, func(*args, **kw)
            except Exception as ept:
                logger.error('[%s] %s' % (text, ept))
            return False, None
        return wrapper
    return decorator


class Spider:
    def __init__(self):
        self.session = requests.session()
        self.base_headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'zhjw.scu.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            'Origin': 'http://zhjw.scu.edu.cn',
        }

        self.urls = {
            'captcha': 'http://zhjw.scu.edu.cn/img/captcha.jpg',
            'login': 'http://zhjw.scu.edu.cn/j_spring_security_check',
            'student_name': 'http://zhjw.scu.edu.cn/student/rollManagement/rollInfo/index',
            'student_pic': 'http://zhjw.scu.edu.cn/main/queryStudent/img?',
            'all_term_scores': 'http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/data',
        }

        self.pattens = {
            'login': re.compile(r'errorCode='),
            'student_name': re.compile(r'title=".*?的照片'),
        }


    @req_logger('try fetch captcha')
    def fetch_captcha(self, filepath: str = None) -> str:
        captcha_resp = self.session.get(self.urls['captcha'])
        assert captcha_resp.status_code == requests.codes.ok, 'Network Issue'
        if filepath:
            with open(filepath, 'wb') as imfile:
                imfile.write(captcha_resp.content)
        return base64Img_encode(captcha_resp.content)

    @req_logger('try login')
    def login(self, stid: str, passwd: str, captcha: str, remb_me: bool) -> None:
        post_data = {
            'j_username': stid,
            'j_password': passwd,
            'j_captcha': captcha,
        }
        if remb_me:
            post_data['_spring_security_remember_me'] = 'on'

        login_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://zhjw.scu.edu.cn/login',
            'X-Requested-With': '',
        }
        login_headers = dict(self.base_headers, **login_headers)

        login_resp = self.session.post(
            url=self.urls['login'], data=post_data, headers=login_headers)
        assert login_resp.status_code == requests.codes.ok, 'Network Issue'

        assert not re.search(
            self.pattens['login'], login_resp.content.decode('utf-8')), '输入信息错误'

    @req_logger('try get student name')
    def fetch_student_name(self) -> str:
        fetname_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://zhjw.scu.edu.cn/'
        }
        fetname_headers = dict(self.base_headers, **fetname_headers)
        fetname_resp = self.session.get(
            url=self.urls['student_name'], headers=fetname_headers)
            
        assert fetname_resp.status_code == requests.codes.ok, 'Network Issue'

        stdname = re.search(
            self.pattens['student_name'], fetname_resp.content.decode('utf-8')
        )
        assert stdname, '没有找到姓名'

        return stdname[0][7:].replace('的照片', '')

    @req_logger('try fetch student picture')
    def fetch_student_pic(self, filepath: str = None) -> str:
        fetpic_headers = {
            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/index'
        }
        fetpic_headers = dict(self.base_headers, **fetpic_headers)
        
        fetpic_resp = self.session.get(url=self.urls['student_pic'], headers=fetpic_headers)
        assert fetpic_resp.status_code == requests.codes.ok, 'Network Issue'
        if filepath:
            with open(filepath, 'wb') as imfile:
                imfile.write(fetpic_resp.content)
        return base64Img_encode(fetpic_resp.content)
    
    @req_logger('try fetch all term scores')
    def fetch_all_term_scores(self, pagesize: int) -> dict:
        fetscores_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/index',
            'X-Requested-With': 'XMLHttpRequest'
        }
        fetscores_headers = dict(self.base_headers, **fetscores_headers)

        if pagesize == -1:
            _, prefetch = self.fetch_all_term_scores(1)
            assert _, 'prefetch error'
            totalCount = prefetch['list']['pageContext']['totalCount']
            _, postfetch = self.fetch_all_term_scores(totalCount)
            assert _, 'postfetch error'
            return postfetch

        post_data = { 'pageSize': pagesize }
        fetpic_resp = self.session.post(
            url=self.urls['all_term_scores'],
            data=post_data,
            headers=fetscores_headers
        )

        return ujson.loads(fetpic_resp.content.decode('utf-8'))
    