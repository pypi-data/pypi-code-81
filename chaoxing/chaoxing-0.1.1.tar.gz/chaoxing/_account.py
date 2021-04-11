'''
Date: 2021-03-25 19:01:10
LastEditors: lisonge
Author: lisonge
LastEditTime: 2021-04-09 15:24:08
'''
import logging
import httpx
from ._exceptions import AuthError
from ._typing import LoginResp, LoginFailedResp, LoginSuccessResp


class ChaoXingClient:
    # uid: int
    cookies: httpx.Cookies
    session: httpx.AsyncClient

    def __init__(self, session: httpx.AsyncClient):
        self.session = session

    async def login(self, username: str, password: str):
        url = 'https://passport2.chaoxing.com/api/login'
        params = {
            'name': username,
            'pwd': password,
            'schoolid': '',
            'verify': '0',
        }
        response = await self.session.get(url, params=params)
        data: LoginResp = response.json()
        if not data['result']:
            data: LoginFailedResp
            raise AuthError(data['errorMsg'])
        data: LoginSuccessResp
        # self.uid = data['uid']
        self.cookies = response.cookies
