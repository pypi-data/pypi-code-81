import math
import time
import random

import requests
from webrequests import WebRequest as WR


class LetPub(object):
    base_url = 'http://www.letpub.com.cn'
    index_url = base_url + '/index.php?page=grant'
    search_url = base_url + '/nsfcfund_search.php'

    def __init__(self):
        self.subcategory_list = self.list_support_types()

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

        print(payload)
        while True:
            soup = WR.get_soup(self.search_url, method='POST', params=params, data=payload)
            if not soup.select_one('#dict div b'):
                print(soup.text)
                time.sleep(10)
                continue
            break

        total_count = int(soup.select_one('#dict div b').text)
        total_page = math.ceil(total_count / 10.)

        print('total count of {}: {}'.format(code, total_count))

        if total_page > 20:
            if not subcategory:
                print('too many result, search with subcategory ...')
                for subcategory in self.subcategory_list:
                    yield from self.search(code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory)
            else:
                print('too many result, please refine your input!')
                exit()

        time.sleep(random.randint(3, 6))

        if total_page > 0:
            print('>>> dealing with page/total page: {}/{}'.format(page, total_page))

            ths = soup.select('table.table_yjfx .table_yjfx_th')
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

            if page < total_page:
                page += 1
                yield from self.search(code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory)
