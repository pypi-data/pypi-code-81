#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 5:39
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : hosted_backend.py
@Desc    : 
"""
import logging
import io
import os
import platform
from contextlib import closing
import requests
from waveletai.envs import CHUNK_SIZE, WARN_SIZE
from multiprocessing.dummy import Pool as ThreadPool
from waveletai.backend import Backend
from waveletai.utils import with_api_exceptions_handler
from waveletai.oauth import WaveletAIAuthenticator
from waveletai.dataset import Dataset, Asset
from waveletai.exceptions import LoginFailed, NotADirectory
from waveletai.constants import DataType
from waveletai.utils.storage_utils import UploadEntry, scan_upload_entries, SilentProgressIndicator, LoggingDownloadProgressIndicator
from waveletai.utils.datastream import FileStream

_logger = logging.getLogger(__name__)

pool = ThreadPool(9)


class HostedBackend(Backend):

    # @with_api_exceptions_handler
    # def __init__(self, api_token=None):
    #     from waveletai import __version__
    #     self.client_lib_version = __version__
    #
    #     self.credentials = Credentials(api_token)
    #
    #     ssl_verify = True
    #     if os.getenv("WAI_ALLOW_SELF_SIGNED_CERTIFICATE"):
    #         urllib3.disable_warnings()
    #         ssl_verify = False
    #
    #     self._http_client = RequestsClient(ssl_verify=ssl_verify)
    #     user_agent = 'waveletai-client/{lib_version} ({system}, python {python_version})'.format(
    #         lib_version=self.client_lib_version,
    #         system=platform.platform(),
    #         python_version=platform.python_version())
    #     self._http_client.session.headers.update({'User-Agent': user_agent})
    #     self._http_client_for_token.session.headers.update({'User-Agent': user_agent})
    #     self._http_client.session.headers.update({'X-TOKEN': })
    #
    #     self.authenticator = self._create_authenticator(self.credentials.api_token, ssl_verify)
    #     self._http_client.authenticator = self.authenticator
    @with_api_exceptions_handler
    def __init__(self, name=None, pwd=None):
        from waveletai import __version__
        self.client_lib_version = __version__
        self._session = requests.session()
        user_agent = 'waveletai-client/{lib_version} ({system}, python {python_version})'.format(
            lib_version=self.client_lib_version,
            system=platform.platform(),
            python_version=platform.python_version())
        headers = {'User-Agent': user_agent}
        res = self._session.post(
            url=f'{self.api_address}/account/users/login/',
            json={'username': name, 'password': pwd},
            headers=headers
        )
        if res.json()["message"]:
            raise LoginFailed(res.json()["message"])
        print("WaveletAI Backend connected")
        self._session.headers.update({"X-TOKEN": res.json()["data"]["token"]})

    @with_api_exceptions_handler
    def _create_authenticator(self, api_token, ssl_verify):
        return WaveletAIAuthenticator(api_token, ssl_verify)

    @property
    def api_address(self):
        return "http://ai.xiaobodata.com/api"
        # return "http://localhost:3000"

    @property
    def display_address(self):
        # return self._client_config.display_url
        pass

    @with_api_exceptions_handler
    def create_dataset(self, name, zone, path, data_type=DataType.TYPE_FILE.value, desc=None):
        res = self._session.post(
            url=f'{self.api_address}/data/dataset/',
            json={'name': name, 'zone': zone, 'type': data_type, 'desc': desc},
        )
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        print(f"Dataset id = {res.json()['data']['id']} created succ")

        dict = res.json()['data']
        self.upload_dataset(dict['id'], path)
        return Dataset(self, dict['id'], dict['name'], dict['desc'], dict['zone'], dict['dimension'], dict['json_data'],
                       dict['create_time'], dict['type'], dict['create_user_id'], dict['update_time'],
                       dict['update_user_id'])

    @with_api_exceptions_handler
    def upload_dataset(self, dataset_id, path):
        """
        :param dataset_id: 文件所属数据集
        :param path: 要上传的文件夹/文件路径
        :return:  上传文件 succ，共xxx个
        """
        entries = scan_upload_entries({UploadEntry(path, "")})
        s_count = f_count = 0
        for entry in entries:
            fs = FileStream(entry)
            progress_indicator = SilentProgressIndicator(fs.length, fs.filename)
            res = self._upload_raw_data(api_method=f'/data/dataset/{dataset_id}/asset', file=fs)
            if res.json()["message"]:
                f_count = f_count + 1
                _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            else:
                # print(f"file {entry.source_path} upload succ")
                progress_indicator.complete()
                s_count = s_count + 1
            fs.close()
        print(f"Dataset id = {dataset_id}  upload succ: {s_count} , fail: {f_count}")

    # @with_api_exceptions_handler
    # def _url_download(self, urls):
    #     url, destination, filename = urls
    #     destination_loc = os.path.join(destination, filename)
    #     with closing(requests.get(url, stream=True)) as response:
    #         chunk_size = 1024  # 单次请求最大值
    #         content_size = int(response.headers['content-length'])  # 内容体总大小
    #         progress = ProgressBar(filename, total=content_size,
    #                                unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
    #         with open(destination_loc, 'wb') as f:
    #             for data in response.iter_content(chunk_size=chunk_size):
    #                 f.write(data)
    #                 progress.refresh(count=len(data))

    @with_api_exceptions_handler
    def _url_download(self, urls):
        url, destination, filename = urls
        destination_loc = os.path.join(destination, filename)
        with closing(requests.get(url, stream=True)) as response:
            content_size = int(response.headers['content-length'])  # 内容体总大小

            progress_indicator = SilentProgressIndicator(content_size, filename)
            if content_size >= WARN_SIZE:
                progress_indicator = LoggingDownloadProgressIndicator(content_size, filename)
            with open(destination_loc, 'wb') as f:
                for data in response.iter_content(chunk_size=CHUNK_SIZE):
                    progress_indicator.progress(CHUNK_SIZE)
                    f.write(data)
        progress_indicator.complete()

    @with_api_exceptions_handler
    def download_dataset_artifact(self, dataset_id, path, destination):
        """
        :param dataset_id:
        :param path:
        :param destination:
        :return:
        """
        pass

    @with_api_exceptions_handler
    def download_dataset_artifacts(self, dataset_id, destination):

        if not destination:
            destination = os.getcwd()

        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)

        try:
            artifacts = self._list_dataset_artifacts(dataset_id)
            urls = []
            for asset in artifacts:
                urls.append((asset.path, destination, asset.name))
            pool.map(self._url_download, urls)
            pool.close()
            pool.join()
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    def _list_dataset_artifacts(self, dataset_id):
        """
        :param dataset_id:
        :return: 返回数据集文件列表
        """
        res = self._session.get(url=f'{self.api_address}/data/dataset/{dataset_id}/asset?page=-1')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        artifacts = []
        for art in res.json()['data']['data']:
            artifacts.append(
                Asset(art['id'], art['name'], art['path'], art['content_type'], art['size'], art['type'], dataset_id))
        return artifacts

    @with_api_exceptions_handler
    def create_model(self, app_id, name, desc):
        pass

    @with_api_exceptions_handler
    def register_model(self, model_id, name, mode, art_id):
        pass

    @with_api_exceptions_handler
    def download_model(self, model_id, version, destination):
        pass

    # def _upload_loop(self, fun, data, progress_indicator, **kwargs):
    #     ret = None
    #     for part in data.generate():
    #         ret = with_api_exceptions_handler(self._upload_loop_chunk)(fun, part, data, **kwargs)
    #         progress_indicator.progress(part.end - part.start)
    #
    #     data.close()
    #     return ret
    #
    #
    # def _upload_loop_chunk(self, fun, part, data, **kwargs):
    #     if data.length is not None:
    #         binary_range = "bytes=%d-%d/%d" % (part.start, part.end - 1, data.length)
    #     else:
    #         binary_range = "bytes=%d-%d" % (part.start, part.end - 1)
    #     headers = {
    #         "Content-Type": "application/octet-stream",
    #         "Content-Filename": data.filename,
    #         "X-Range": binary_range,
    #     }
    #     if data.permissions is not None:
    #         headers["X-File-Permissions"] = data.permissions
    #     response = fun(data=part.get_data(), headers=headers, **kwargs)
    #     response.raise_for_status()
    #     return response

    # import requests
    #
    # url = "localhost:3000/rest/market/upload"
    #
    # payload = {'type': 'video',
    #            'task_id': 'test1',
    #            'chunk': '1'}
    # files = [
    #     ('file', ('video.mp4', open('/C:/Users/janus/Desktop/video.mp4', 'rb'), 'application/octet-stream'))
    # ]
    # headers = {
    #     'Content-Type': 'multipart/form-data'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload, files=files)
    #
    # print(response.text)

    def _upload_raw_data(self, api_method, file: FileStream, headers={}, data={}):
        url = self.api_address + api_method
        res = self._session.post(url=url,
                                 files=[('file', (
                                     file.filename.replace(".\\", ""), open(file.fobj.name, 'rb'), file.content_type))],
                                 data=data,
                                 headers=headers)
        return res

    def _download_raw_data(self, api_method, headers, path_params, query_params):
        url = self.api_address + api_method.operation.path_name + "?"

        for key, val in path_params.items():
            url = url.replace("{" + key + "}", val)

        for key, val in query_params.items():
            url = url + key + "=" + val + "&"

        session = self._session

        request = self.authenticator.apply(
            requests.Request(
                method='GET',
                url=url,
                headers=headers
            )
        )

        return session.send(session.prepare_request(request), stream=True)

    @with_api_exceptions_handler
    def _upload_tar_data(self, experiment, api_method, data):
        url = self.api_address + api_method.operation.path_name
        url = url.replace("{experimentId}", experiment.internal_id)

        session = self._http_client.session

        request = self.authenticator.apply(
            requests.Request(
                method='POST',
                url=url,
                data=io.BytesIO(data),
                headers={
                    "Content-Type": "application/octet-stream"
                }
            )
        )

        response = session.send(session.prepare_request(request))
        response.raise_for_status()
        return response
