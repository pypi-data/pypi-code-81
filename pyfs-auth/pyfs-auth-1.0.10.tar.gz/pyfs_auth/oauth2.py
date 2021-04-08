# -*- coding: utf-8 -*-

from pyfs_base import BaseFeishu


class OAuth2(BaseFeishu):
    def __init__(self):
        super(OAuth2, self).__init__()
        # 移动应用接入 - 接入流程, Refer: https://open.feishu.cn/document/uAjLw4CM/uYjL24iN/mobile-app/mobile-app-overview
        # 第二步：获取 access_token
        self.SUITE_PASSPORT_OAUTH_TOKEN = self.PASSPORT_DOMAIN + '/suite/passport/oauth/token'
        # 第三步：获取用户信息
        self.SUITE_PASSPORT_OAUTH_USERINFO = self.PASSPORT_DOMAIN + '/suite/passport/oauth/userinfo'

    def get_access_info(self, code=None, grant_type='authorization_code', appid=None, client_id=None, secret=None, client_secret=None, code_verifier=None):
        return self.post(self.SUITE_PASSPORT_OAUTH_TOKEN, data={
            'grant_type': grant_type,
            'client_id': client_id or appid,
            'client_secret': client_secret or secret,
            'code': code,
            'code_verifier': code_verifier,
        }, content_type='application/x-www-form-urlencoded')

    def get_userinfo(self, access_token=None, code=None, grant_type='authorization_code', appid=None, client_id=None, secret=None, client_secret=None, code_verifier=None):
        if not access_token:
            access_token = self.get_access_info(code=code, grant_type=grant_type, appid=appid, client_id=client_id, secret=secret, client_secret=client_secret, code_verifie=code_verifier).get('access_token')
        return self.post(self.SUITE_PASSPORT_OAUTH_USERINFO, data={
            'token': access_token,
        })


oauth2 = OAuth2()
get_access_info = oauth2.get_access_info
get_userinfo = oauth2.get_userinfo
