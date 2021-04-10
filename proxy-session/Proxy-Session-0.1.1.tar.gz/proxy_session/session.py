import requests
# import ipaddress
from bs4 import BeautifulSoup
from random import choice
import sys
from urllib.parse import urlparse


class ProxySessionTimeout():
    QUICK_TIMEOUT = 3
    SHORT_TIMEOUT = 5
    LENGTHY_TIMEOUT = 10
    LONG_TIMEOUT = 20
    VERY_LONG_TIMEOUT = 30
    NO_TIMEOUT = 24*3600
    DEFAULT_TIMEOUT = None


class ProxySession(requests.Session):
    def __init__(self, user_=None, pass_=None, socks=False):
        '''
        @param user_: str[None] -> Username for proxy authentication
        @param pass_: str[None] -> Password for proxy authentication
        @param socks: bool[False] -> If True, it will perform a socks5
                authentication, given the user_ and pass_ has been
                provided. If False, it will perform a basic authent-
                ication will be performed, provided the value of
                user_ and pass_.
        '''
        super(ProxySession, self).__init__()
        self.__error__ = None
        if pass_ is None or pass_ is None:
            self.__user__, self.__pass__ = None, None
            self.socks = False
        elif isinstance(pass_, str) and isinstance(pass_, str):
            self.__user__, self.__pass__ = user_, pass_
            self.socks = socks
        else:
            raise TypeError('pass_ and pass_ should be a string')
        
        self.__proxy_servers__ = list()
        self.__tried_proxies__ = list()
        self.__current_proxy__ = None
    
    # def __get_proxy_server__(self, addr):
    #     try:
    #         broken_proxy_host = addr[::-1].split(':')
    #         rev_port, rev_host = broken_proxy_host[0], broken_proxy_host[1:]
    #         port = int(rev_port[::-1])
    #         ip_addr = ipaddress.ip_address(':'.join(rev_host)[::-1])
    #         return ip_addr, port
    #     except ValueError as e:
    #         return None

    def __collect_proxy_server_list__(self):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        try:
            response = requests.get('https://free-proxy-list.net/', headers=headers)
        except Exception as e:
            response = type('EmptyResponse', tuple(), {
                'status_code' : -1,
                'text' : f'{e}'
            })
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html5lib')
            proxy_list_table = soup.find('table', attrs={'id' : 'proxylisttable'})
            proxy_list_tbody = proxy_list_table.find('tbody')
            proxy_list_trows = proxy_list_tbody.find_all('tr')
            for proxy_list_trow in proxy_list_trows:
                proxy_row_data = proxy_list_trow.find_all('td')
                proxy_host = proxy_row_data[0].contents[0].strip()
                proxy_port = proxy_row_data[1].contents[0].strip()
                proxy_protocol = proxy_row_data[6].contents[0].strip()
                self.__proxy_servers__.append(
                   ("http" if proxy_protocol == "no" else "https",
                   f'{"socks5" if self.socks else "http"}://{self.__PROXY_AUTH__}{proxy_host}:{proxy_port}')
                )
            self.__error__ = None
        else:
            self.__error__ = response.status_code, response.text

    @property
    def error(self):
        return self.__error__

    def __enter__(self):
        super(ProxySession, self).__enter__()
        self.__collect_proxy_server_list__()
        return self

    @property
    def __PROXY_AUTH__(self):
        if self.__user__ is not None and self.__pass__ is not None:
            return f'{self.__user__}:{self.__pass__}@'
        else:
            return ''
    
    def make_request(self, url, method='GET', timeout=ProxySessionTimeout.SHORT_TIMEOUT, log = True, max_attempt = 100, **kwargv):
        '''
        @param url: str -> The target URL
        @param method: str[GET] -> The HTTP method to be called
        @param timeout: int[5] -> The timeout value, for the proxy request
        @param log: bool[True] -> It will log the necessary information
        @param max_attempt: int[100] -> Maximum number of attempt to reach the target URL,
                must be a positve integer
        @param **kwargv -> Other keyword arguments, which will be passed to requests.request
                method
        
        @return -> It will always return the tuple of two element, response and proxy_url
            On success, it will return the reponse object, returned by the method call and
            the proxy url. If the random proxy selection is made, it will return the proxy
            url as a string, otherwise it will be same as keyword argument "proxies". 
            On Failure after maximum attempts, it will return a Response object, having
            status_code -1 with empty content. The proxy url will be null in this case.
        '''
        if not isinstance(timeout, int):
            raise TypeError('timeout must be either None or int value')
        else:
            kwargv['timeout'] = timeout

        if not isinstance(max_attempt, int):
            raise ValueError('max_attempt should have a positive integer value')
        elif max_attempt < 1:
            raise ValueError('max_attempt should have a positive integer value')
        
        if kwargv.get('proxies') is not None:
            do_random_proxy_selection = False
        else:
            do_random_proxy_selection = True

        attempt_count = 0
        parsed_url = urlparse(url)
        if parsed_url.scheme == '':
            scheme = 'http'
        else:
            scheme = parsed_url.scheme

        while attempt_count < max_attempt:
            try:
                if do_random_proxy_selection:
                    try:
                        if self.__current_proxy__ is None:
                            self.__current_proxy__ = choice(self.__proxy_servers__)
                        if scheme != self.__current_proxy__[0]:
                            self.__tried_proxies__.append(self.__current_proxy__)

                        if self.__current_proxy__ in self.__tried_proxies__:
                            self.__proxy_servers__.remove(self.__current_proxy__)
                            self.__current_proxy__ = None
                            continue
                    except IndexError:
                        _proxy_collection_attempt = 0
                        while _proxy_collection_attempt < 3:
                            self.__current_proxy__ = None
                            self.__tried_proxies__.clear()
                            self.__proxy_servers__.clear()
                            self.__collect_proxy_server_list__()
                            _proxy_collection_attempt+=1
                            if self.__error__ is None:
                                break
                        if _proxy_collection_attempt == 3:
                            break 
                        continue

                    if self.__current_proxy__ is not None:
                        if log: print(f'Trying random free proxy[{self.__current_proxy__[0]}]: {self.__current_proxy__[1]}')
                        try:
                            kwargv['proxies'] = {
                                self.__current_proxy__[0] : self.__current_proxy__[1],
                            }
                            response = requests.request(method, url, **kwargv)
                            return response, self.__current_proxy__[1]
                        except ValueError as e:
                            if log: print(e, file=sys.stderr)
                            raise requests.exceptions.ProxyError(f'ValueError - {e}')
                else:
                    if log: print(f'Proxy server: [{kwargv.get("proxies")}]')
                    try:
                        response = requests.request(method, url, **kwargv)
                        return response, kwargv.get('proxies')
                    except ValueError as e:
                        if log: print(e, file=sys.stderr)
                        raise requests.exceptions.ProxyError(f'ValueError - {e}')
            except (requests.exceptions.Timeout, requests.exceptions.ProxyError):
                if do_random_proxy_selection:
                    self.__tried_proxies__.append(self.__current_proxy__)
                    self.__tried_proxies__.remove(self.__current_proxy__)
                    self.__current_proxy__ = None
                    kwargv['proxies'].clear()
            attempt_count+=1
        return type('EmptyResponse', tuple(), {
            'status_code' : -1,
            'content' : b'',
            'text' : '',
            '__str__' : lambda this: f'<EmptyResponse {url} -1>',
            '__repr__': lambda this: f'<EmptyResponse {url} -1>',
            '__format__': lambda this, *argv: f'<EmptyResponse {url} -1>'
        })(), None
    
    