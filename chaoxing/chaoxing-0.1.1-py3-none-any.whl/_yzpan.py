'''
Date: 2021-03-25 19:48:54
LastEditors: lisonge
Author: lisonge
LastEditTime: 2021-04-09 16:09:50
'''
from ._logging import logging
import httpx
from ._typing import YzPanUserValidResp, YzPanUploadResp
from ._exceptions import YzPanAuthError
from ._account import ChaoXingClient
from typing import overload, Union, IO, List


class YzPanClient:
    token: str
    uid: int
    session: httpx.AsyncClient

    def __init__(self, session: httpx.AsyncClient):
        self.session = session

    async def login(self, chaoxingClient: ChaoXingClient):
        cookies = chaoxingClient.cookies
        url = 'https://pan-yz.chaoxing.com/api/token/uservalid'
        response = await self.session.get(url, cookies=cookies)
        data: YzPanUserValidResp = response.json()
        if not data['result']:
            raise YzPanAuthError(data)
        self.token = data['_token']
        uid = cookies.get('UID', domain='.chaoxing.com')
        if uid == None:
            raise YzPanAuthError('cookies must have name <UID>')
        self.uid = int(uid)

    async def upload_file(
        self,
        fileName: str,
        folderId: str,
        content: Union[str, bytes, IO[bytes], IO[str]]
    ) -> YzPanUploadResp:
        url = 'https://pan-yz.chaoxing.com/upload/uploadfile'
        params = {
            '_token': self.token,
        }
        data = {
            'puid': str(self.uid),
            'name': fileName,
            'type': f'image/{fileName.split(".")[-1]}',
            'fldid': folderId,
        }
        files = {
            'file': (fileName, content),
        }
        response = await self.session.post(
            url,
            params=params,
            data=data,
            files=files
        )
        data: YzPanUploadResp = response.json()
        return data

    async def delete_files(self, resIdList: List[int]):
        url = 'https://pan-yz.chaoxing.com/api/delete'
        resids = ','.join(map(lambda el: str(el), resIdList))
        params = {
            'puid': str(self.uid),
            '_token': self.token,
            'resids': resids,
        }
        await self.session.get(url, params=params)

    async def rename(self, resId: int, name: str):
        url = 'https://pan-yz.chaoxing.com/opt/rename'
        params = {
            'resid': str(resId),
            'name': name,
            'puid': str(self.uid),
        }
        await self.session.post(url, params=params)
