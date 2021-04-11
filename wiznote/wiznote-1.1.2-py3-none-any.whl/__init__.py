# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/15 22:33
# @Author  : https://github.com/536
from .core import API


class Wiz(API):
    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self):
        """用户登录"""
        return self.session.post(
            self.url('{AS_URL}/as/user/login'),
            json={
                'userId': self.username,
                'password': self.password
            }
        )

    def get_userinfo_by_token(self):
        """通过有效的token，获取用户信息"""
        return self.session.post(
            self.url('{AS_URL}/as/user/login/token')
        )

    def logout(self):
        """注销token"""
        return self.session.get(
            self.url('{AS_URL}/as/user/logout')
        )

    def get_userinfo(self):
        """获取用户信息"""
        return self.session.get(
            self.url('{AS_URL}/as/user/info')
        )

    def keep(self):
        """延长token有效期"""
        return self.session.get(
            self.url('{AS_URL}/as/user/keep')
        )

    def token2temp(self):
        """通过当前token获取一个临时id

        然后通过这个id，在60秒内可以重新拿到token。该id一次有效，使用后就会失效。
        可以用于跨域页面跳转，避免泄漏token
        """
        return self.session.get(
            self.url('{AS_URL}/as/token/token2temp')
        )

    def get_token_by_tokenid(self, tempToken):  # NOQA
        """通过tokenid获取token"""
        return self.session.get(
            self.url('{AS_URL}/as/token/temp2token'),
            params={
                'tempToken': tempToken
            }
        )

    def get_avatar(self):
        """获取用户头像"""
        return self.session.get(
            self.url('{AS_URL}/as/user/avatar/{userGuid}',
                     userGuid=self.userGuid)
        )

    def get_cert(self):
        """获取用户的加密笔记证书"""
        return self.session.get(
            self.url('{AS_URL}/as/user/cert')
        )

    def get_shares(self, pageIndex=0, pageSize=10):
        """获取分享列表"""
        return self.session.get(
            self.url('{AS_URL}/share/api/shares'),
            params={
                'page': pageIndex,
                'size': pageSize,
                'kb_guid': self.kbGuid
            }
        )

    def get_share(self, docGuid):
        """获取某一个分享详情"""
        return self.session.get(
            self.url('{AS_URL}/share/api/shares'),
            params={
                'kb_guid': self.kbGuid,
                'docGuid': docGuid
            }
        )

    def clone_share(self, shareId):
        """保存分享的内容到用户自己的笔记中"""
        return self.session.get(
            self.url('{AS_URL}/share/api/shares/{shareId}/clone', shareId=shareId)
        )

    def download_note(self, docGuid, downloadInfo=0, downloadData=0):
        """下载笔记"""
        return self.session.get(
            self.url('{kbServer}/ks/note/download/{kbGuid}/{docGuid}',
                     docGuid=docGuid,
                     downloadData=downloadData,
                     downloadInfo=downloadInfo),
            params={
                'downloadInfo': downloadInfo,
                'downloadData': downloadData,
            }
        )

    def get_note_res(self, docGuid, resName):
        """获取某一个笔记资源数据，用于直接在浏览器内显示笔记内容"""
        return self.session.get(
            self.url('{kbServer}/ks/note/view/{kbGuid}/{docGuid}/index_files/{resName}',
                     docGuid=docGuid,
                     resName=resName)
        )

    def get_note_view(self, docGuid):
        """获取笔记html，用户在浏览器内直接显示笔记"""
        return self.session.get(
            self.url('{kbServer}/ks/note/view/{kbGuid}/{docGuid}/',
                     docGuid=docGuid)
        )

    def get_note_info(self, docGuid):
        """获取笔记信息"""
        return self.session.get(
            self.url('{kbServer}/ks/note/info/{kbGuid}/{docGuid}/',
                     docGuid=docGuid)
        )

    def get_note_attachments(self, docGuid):
        """获取某一个笔记的附件列表"""
        return self.session.get(
            self.url('{kbServer}/ks/note/attachments/{kbGuid}/{docGuid}',
                     docGuid=docGuid)
        )

    def get_kb_info(self):
        """获取kb信息"""
        return self.session.get(
            self.url('{kbServer}/ks/kb/info/{kbGuid}')
        )

    def get_kb_documents(self):
        """获取某一个kb的笔记数量"""
        return self.session.get(
            self.url('{kbServer}/ks/kb/{kbGuid}/document/count')
        )

    def get_shared_notes(self, docGuid):
        """获取公开群组笔记html"""
        return self.session.get(
            self.url('{kbServer}/ks/share/group/note/{kbGuid}/{docGuid}',
                     docGuid=docGuid)
        )

    def search_shared_notes(self, searchText):
        """搜索公开群组笔记"""
        return self.session.get(
            self.url('{kbServer}/ks/note/share/search/{kbGuid}?ss={searchText}',
                     searchText=searchText)
        )

    def search_notes(self, searchText):
        """搜索笔记"""
        return self.session.get(
            self.url('{kbServer}/ks/note/search/{kbGuid}?ss={searchText}',
                     searchText=searchText)
        )

    def get_tags(self):
        """获取全部标签"""
        return self.session.get(
            self.url('{kbServer}/ks/tag/all/{kbGuid}')
        )

    def get_category(self):
        """获取所有文件夹"""
        return self.session.get(
            self.url('{kbServer}/ks/category/all/{kbGuid}')
        )

    def get_note_abstract(self, docGuid):
        """获取笔记图片缩略图，如果不存在报告404"""
        return self.session.get(
            self.url('{kbServer}/ks/note/abstract/{kbGuid}/{docGuid}',
                     docGuid=docGuid)
        )

    def download(self, docGuid):
        """下载加密笔记数据，笔记资源，附件数据，笔记缩略图"""
        return self.session.get(
            self.url('{kbServer}/ks/object/download/{kbGuid}/{docGuid}?objType=document',
                     docGuid=docGuid)
        )

    def get_history(self, docGuid, objType, objGuid):
        """获取笔记/附件历史版本列表

        :type objType: document|attachment
        :type objGuid: docGuid|attGuid
        """
        return self.session.get(
            self.url('{kbServer}/ks/history/list/{kbGuid}/{docGuid}?objType={objType}&objGuid={objGuid}',
                     docGuid=docGuid,
                     objGuid=objGuid,
                     objType=objType)
        )

    def get_notes_of_folder(self, category, withAbstract, start, count, orderBy='created', ascending='desc'):
        """获取某一个文件夹下面的笔记列表

        :type category: folder
        :type withAbstract: true|false
        :type orderBy: title|created|modified
        :type ascending: asc|desc
        """
        return self.session.get(
            self.url('{kbServer}/ks/note/list/category/{kbGuid}'),
            params={
                'category': category,
                'withAbstract': withAbstract,
                'start': start,
                'count': count,
                'ascending': ascending,
                'orderBy': orderBy,
            }
        )

    def get_notes_of_tag(self, tagGuid, withAbstract, start, count, orderBy='created', ascending='desc'):
        """获取某一个标签下面的笔记列表

        :type tagGuid: tagGuid
        :type withAbstract: true|false
        :type orderBy: title|created|modified
        :type ascending: asc|desc
        """
        return self.session.get(
            self.url('{kbServer}/ks/note/list/tag/{kbGuid}'),
            params={
                'tag': tagGuid,
                'withAbstract': withAbstract,
                'start': start,
                'count': count,
                'ascending': ascending,
                'orderBy': orderBy,
            }
        )
