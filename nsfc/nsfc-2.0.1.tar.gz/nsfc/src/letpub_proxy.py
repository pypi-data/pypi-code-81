import os
import math
import time
import json
import random

import bs4
import requests
from webrequests import WebRequest as WR


class LetPub(object):
    base_url = 'http://www.letpub.com.cn'
    index_url = base_url + '/index.php?page=grant'
    search_url = base_url + '/nsfcfund_search.php'

    proxy_url = 'http://127.0.0.1:5010/'
    proxy_cache = 'proxy_pool.json'

    def __init__(self):
        self.subcategory_list = self.list_support_types()
        self.proxy_pool = self.get_proxy_pool()

    def list_support_types(self):
        """项目类别列表
        """
        soup = WR.get_soup(self.index_url)
        options = soup.select('select#subcategory option')
        subcategory_list = [option.text for option in options[1:]]
        return subcategory_list
    

    def search(self, code, page=1, start_year='', end_year='', subcategory=''):
        """项目查询，最多显示20页(200条)，超出时增加项目类别细分查询
        """
        params = {
            'mode': 'advanced',
            'datakind': 'list',
            'currentpage': page
        }

        payload = {
            'addcomment_s1': code[0],
            'startTime': start_year,
            'endTime': end_year,
            'searchsubmit': 'true',
            'subcategory': subcategory,
        }
        level = math.ceil(len(code) / 2.)
        payload.update({
            'addcomment_s{}'.format(level): code
        })

        soup = self.search_page(params, payload)
        total_count = int(soup.select_one('#dict div b').text)
        total_page = math.ceil(total_count / 10.)

        print('total count: {} [{}]'.format(total_count, payload))
        if 0 < total_page <= 20:
            print('>>> dealing with page: {}/{} [{}]'.format(page, total_page, payload))
            yield from self.parse_content(soup)
        elif total_page > 20:
            if not subcategory:
                print('too many result, search with subcategory ...')
                for subcategory in self.subcategory_list:
                    yield from self.search(code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory)
            else:
                print('too many result, please refine your input!')
                exit(1)

        if page < total_page:
            page += 1
            time.sleep(random.randint(3, 6))
            yield from self.search(code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory)

    def parse_content(self, soup):
        """项目内容解析
        """
        ths = soup.select('table.table_yjfx .table_yjfx_th')
        if ths:
            title = [th.text for th in ths]
            context = {}
            for tr in soup.select('table.table_yjfx tr')[2:-1]:
                values = [td.text for td in tr.select('td')]
                if len(values) == len(title):
                    if context:
                        yield context
                    context = dict(zip(title, values))
                else:
                    context.update(dict([values]))
            yield context

    def search_page(self, params, payload, use_proxy=True):
        """查询页面
        """
        # print(params, payload)
        while True:
            if use_proxy:
                proxy = random.choice(self.proxy_pool)
                proxies = {'http': proxy}
                print('>>> use proxy: {}'.format(proxy))
                try:
                    resp = requests.post(self.search_url, params=params, data=payload, proxies=proxies, timeout=10)
                    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
                except Exception as e:
                    self.proxy_pool.remove(proxy)
                    continue
            else:
                soup = WR.get_soup(self.search_url, method='POST', params=params, data=payload)

            if not soup.select_one('#dict div b'):
                print('*****', soup.text)
                time.sleep(5)
                continue
            return soup


    def get_proxy_pool(self):
        url = self.proxy_url + '/get_all/'
        if os.path.isfile(self.proxy_cache):
            with open(self.proxy_cache) as f:
                proxy_pool = json.load(f)
        else:
            data = requests.get(url).json()
            proxy_pool = []
            for each in data:
                proxy = 'http://' + each['proxy']
                print(f'>>> checking proxy: {proxy}')
                try:
                    resp = requests.get(self.base_url, proxies={'http': proxy}, timeout=5)
                    print('ok')
                    proxy_pool.append(proxy)
                except:
                    # print('bad')
                    pass
            with open(self.proxy_cache, 'w') as out:
                json.dump(proxy_pool, out, indent=2)
        print('proxy pool: {}'.format(len(proxy_pool)))
        return proxy_pool


'''
proxies not work ???
'''