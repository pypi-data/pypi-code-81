# -*- coding: utf-8 -*-
# features.py

"""
Module complémentaire
============================

pathfile : dreamtools/features.py

"""
import re
import requests

from urllib.parse import urljoin

from . import tools
from .logmng import CTracker


def test_http_link(url):
    """ Vérifie une url et renvoie l'url valide

    :param url: url à évaluer
    :rtype str:
    """

    def fn():
        s = tools.clean_space(url)

        if not re.match(r'^https?[:]//', s):
            s = f'http://{s}'

        ret = requests.head(s)

        if ret.status_code in [301, 302]:
            return test_http_link(ret.headers.get('Location'))

        return s if (ret.status_code == requests.codes.ok) else False

    return CTracker.fntracker(fn, 'URL Checker').data


def url_join(domaine, page):
    """
    Generation d'une url
    """

    return urljoin(domaine, page)
