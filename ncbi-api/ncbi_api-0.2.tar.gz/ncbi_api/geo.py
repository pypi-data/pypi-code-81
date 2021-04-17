# -*- coding: utf-8 -*-

"""
Author     : ZhangYafei
Description: Geo数据下载
"""
import asyncio
import os
from collections.abc import Iterable
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import async_timeout
from lxml import etree
from requests import Session
from tqdm import tqdm
from zyf.timer import Timeit


class GeoDataType:
    SeriesMatrix = 1


class GeoDownloader:
    def __init__(self, accession_list: Iterable = None):
        self.session = Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76'}
        self.session.headers = self.headers
        self.data_dir = 'download'
        self.history_dir = 'history'

        self.success_f = None
        self.error_f = None
        self.error_list = []
        self.accession_list = set(accession_list) if accession_list else None
        self.func_download_map = {}
        self.func_init_map = {}
        self.init_func_map()

        if not os.path.exists(self.history_dir):
            os.mkdir(self.history_dir)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def init_func_map(self):
        self.func_download_map[GeoDataType.SeriesMatrix] = self.download_series_matrix
        self.func_init_map[GeoDataType.SeriesMatrix] = self.download_series_matrix_init

    def get_download_func(self, date_type: str):
        return self.func_download_map.get(date_type, None)

    @Timeit(prefix='成功读取并完成过滤')
    def filter_request_list(self, request_list: set, desc: str = 'Accession', success_filepath: str = None,
                            error_filepath=None):
        """ 读取并过滤 request 列表 """
        success_filepath = success_filepath if success_filepath else f'{self.history_dir}/success.txt'
        error_filepath = error_filepath if error_filepath else f'{self.history_dir}/error.txt'
        print('-*-' * 22)
        print(f'正在读取 {desc} 列表')
        total_request_count = len(request_list)
        filter_string = f'\t--> 共有 {desc} 数量：{total_request_count}'
        if os.path.exists(success_filepath):
            self.success_f = open(success_filepath, mode='a+')
            self.success_f.seek(0)
            downloaded_request_list = {line.strip() for line in self.success_f}
            request_list = request_list - downloaded_request_list
            filter_string += f', 成功下载：{len(downloaded_request_list)}'
        else:
            self.success_f = open(success_filepath, mode='a+')

        if os.path.exists(error_filepath):
            self.error_f = open(error_filepath, mode='a+')
            self.error_f.seek(0)
            error_request_list = {line.strip() for line in self.error_f}
            request_list = request_list - error_request_list
            filter_string += f', 下载失败(404)：{len(error_request_list)},  还剩：{len(request_list)}'
        else:
            self.error_f = open(error_filepath, mode='a+')
        print(filter_string)
        print('-*-' * 22)
        return request_list

    def download_series_matrix_url(self, accession_list: Iterable = None, series_matrix_url_filepath: str = None,
                                   success_filepath: str = None, error_filepath: str = None, async_on: bool = False):
        if accession_list and type(accession_list) != set:
            accession_list = set(accession_list)
        elif self.accession_list:
            accession_list = self.accession_list
        else:
            raise Exception("accession_list can't is None")

        success_filepath = success_filepath if success_filepath else f'{self.history_dir}/accession_series_matrix_url_success.txt'
        error_filepath = error_filepath if error_filepath else f'{self.history_dir}/accession_series_matrix_url_error.txt'
        self.series_matrix_url_filepath = series_matrix_url_filepath if series_matrix_url_filepath else f'{self.history_dir}/series_matrix_urls.txt'
        self.series_matrix_url_f = open(self.series_matrix_url_filepath, mode='a')
        while True:
            accession_list = self.filter_request_list(request_list=accession_list, desc='Accession',
                                                      success_filepath=success_filepath, error_filepath=error_filepath)
            if len(accession_list) > 0:
                if async_on:
                    asyncio.run(self.download_series_matrix_url_init_async())
                else:
                    with ThreadPoolExecutor(max_workers=10) as pool:
                        futures_list = (pool.submit(self.get_series_matrix_url, accession) for accession in
                                        accession_list)
                        for future in futures.as_completed(futures_list):
                            if isinstance(future.result(), Exception):
                                print(future.result())
            else:
                break
        self.success_f.close()
        self.error_f.close()
        self.series_matrix_url_f.close()

    def get_series_matrix_url(self, accession):
        """ 请求Series_matrix url """
        url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{accession[:-3]}nnn/{accession}/matrix/'
        print(url)
        response = self.session.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            href_list = html.xpath('//pre/a[position() > 1]/@href')
            for href in href_list:
                series_matrix_url = f'{url}{href}'
                self.series_matrix_url_f.write(f'{series_matrix_url}\n')
            self.success_f.write(f'{accession}\n')
            self.series_matrix_url_f.flush()
            self.success_f.flush()
        elif response.status_code == 404:
            self.error_f.write(f'{accession}\n')
            self.error_f.flush()

        print(accession, response.status_code)

    async def download_series_matrix_url_init_async(self, accession_list):
        """ 异步下载 series_matrix_url 初始化"""
        conn = aiohttp.TCPConnector(ssl=False, limit=100, use_dns_cache=True)
        semaphore = asyncio.Semaphore(50)
        async with aiohttp.ClientSession(connector=conn, headers=self.headers) as session:
            await asyncio.gather(
                *[asyncio.create_task(self.get_series_matrix_url_async(session, accession, semaphore)) for accession in
                  accession_list])

    async def get_series_matrix_url_async(self, session, accession, semaphore):
        """ 异步下载 series_matrix url """
        url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{accession[:-3]}nnn/{accession}/matrix/'
        print(url)
        try:
            async with semaphore:
                with async_timeout.timeout(60):
                    async with session.get(url=url) as response:
                        if response.status == 200:
                            text = await response.text()
                            html = etree.HTML(text)
                            href_list = html.xpath('//pre/a[position() > 1]/@href')
                            for href in href_list:
                                series_matrix_url = f'{url}{href}'
                                self.series_matrix_url_f.write(f'{series_matrix_url}\n')
                            self.success_f.write(f'{accession}\n')
                            self.series_matrix_url_f.flush()
                            self.success_f.flush()
                        elif response.status == 404:
                            self.error_f.write(f'{accession}\n')
                            self.error_f.flush()
                        print(accession, response.status)
        except Exception as e:
            print(f'{accession} 请求失败', e)

    def download_series_matrix_init(self, series_matrix_url_filepath: str = None):
        """ 下载series_matrix 初始化 """
        if not series_matrix_url_filepath:
            self.download_series_matrix_url()
        self.series_matrix_url_filepath = series_matrix_url_filepath if series_matrix_url_filepath else f'{self.history_dir}/series_matrix_urls.txt'
        with open(self.series_matrix_url_filepath, mode='r') as f:
            url_list = {line.strip() for line in f}
        return self.filter_request_list(request_list=url_list, desc='url')

    def download_series_matrix(self, url):
        """ 下载series_matrix """
        response = self.session.get(url=url, stream=True)
        if response.status_code != 200:
            print(f'\n{url}\t请求失败\t{response.status_code}')
            if response.status_code == 404:
                self.error_f.write(f'{url}\n')
                self.error_f.flush()
            return

        self.save_to_file(response=response, url=url)

    def save_to_file(self, response, url):
        """ 保存到文件 """
        filename = url.rsplit('/', maxsplit=1)[-1]
        content_size = int(response.headers['content-length'])

        content_size_string = f'{content_size / (1024 * 1024):.2f} MB' if content_size >= (
                1024 * 1024) else f'{content_size / 1024:.2f} KB'

        task_progressbar = tqdm(iterable=response.iter_content(1024), total=int(content_size / 1024), ncols=100,
                                unit='KB', desc=f'正在下载 -> {filename} -> {content_size_string}')
        with open(f'{self.data_dir}/{filename}', 'wb+') as f:
            for chunk in task_progressbar:
                f.write(chunk)

        self.success_f.write(f'{url}\n')
        self.success_f.flush()

    def run(self, data_type, workers: int = None, *args, **kwargs):
        if not data_type:
            raise Exception("data_type can't is None")
        func_execute = self.get_download_func(data_type)
        if not func_execute:
            raise Exception('data_type error, must be ncbi.geo.GeoDataType elements')

        if data_type in self.func_init_map:
            url_list = self.func_init_map[data_type](*args, **kwargs)
        elif self.accession_list:
            url_list = self.accession_list
        else:
            raise Exception('init func or accession_list must one is not None!')

        workers = workers if workers else os.cpu_count()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures_list = (pool.submit(func_execute, url) for url in url_list)
            for future in futures.as_completed(futures_list):
                if future.exception():
                    print(future.exception())

    def __del__(self):
        self.success_f.close()
        self.error_f.close()
