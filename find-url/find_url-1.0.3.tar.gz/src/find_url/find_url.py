# -*- coding: utf-8 -*-

import requests

class Tse:
    def __init__(self):
        self.author = 'Sergey039'

class url(Tse):
    """docstring for url"""
    def __init__(self, url, f, f2):
        self.url = url
        self.f = f
        self.f2 = f2

    def find(url, f, f2):
        try:
            j = requests.get(url).text
            j2 = j.index(f) + len(f)
            result = j[j2:]
            result = result[:99999]
            j2 = result.index(f2)
            result2 = result[:j2]
            res = str(result2)
        except ValueError:
            res = 'Данные с данного сайта не найдены, проверьте код элемента!'
        return res

    def html(html, f, f2):
        try:
            j = html
            j2 = j.index(f) + len(f)
            result = j[j2:]
            result = result[:99999]
            j2 = result.index(f2)
            result2 = result[:j2]
            res = str(result2)
        except ValueError:
            res = 'Данные с данного сайта не найдены, проверьте код элемента!'
        return res

if __name__ == "__main__":
    pass
