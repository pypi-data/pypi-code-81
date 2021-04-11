import requests, random
from .config import *
from selenium import webdriver

class Request():
    """This is a class that handles http requests."""

    def __init__(self):
        """initialize"""
        self.session = requests.Session()

    def getProxy(self):
        """get proxy ip"""
        proxy = {}
        if 'PROXY_API' in globals() and PROXY_API != '':
            req = self.session.get(PROXY_API)
            ipStr = req.text
            if ipStr != '':
                ipList = ipStr.split('--')
                proxy = {ipList[2]: ipList[0] + ':' + ipList[1]}
        else:
            if 'PROXIES' in globals():
                proxyLen = len(PROXIES)
                if proxyLen > 0:
                    proxy = random.sample(PROXIES, 1)[0]
        return proxy

    def getHeader(self):
        """get client information"""
        header = {}
        if 'HEADERS' in globals():
            headerLen = len(HEADERS)
            if headerLen > 0:
                header = random.sample(HEADERS, 1)[0]
        return header

    def get(self, url, data = {}, referer = '', cookies = {}):
        """http get request"""
        header = self.getHeader()
        header['Referer'] = referer
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        header['cookie'] = '''ali_apache_id=11.180.122.26.159688938696.196789.8; acs_usuc_t=x_csrf=pdy8_rq7yg09&acs_rt=85f12becf7e848eabaf377b16055e6ef; intl_locale=en_US; aep_usuc_f=site=glo&c_tp=USD&region=CN&b_locale=en_US; xman_t=REmXdgRStRkg3ENFl+sjnaHT9VOnK8Urzf8LBxgWp3XvdMPvObb4+3N/mf0BE6Q/; xman_f=SbXfK6h6ccTRlU3pYGSBmCkHVFpP6qeDB+OVhAtnFBtGN5lUXPcZKkaqhmoeoXBuD9mX0tNlUi60Pe3dINQCT+TdL2rKyjaJOkJF9pgxjSG30Qo3ziUJfQ==; cna=LIe1F/bbu38CAbbIjJFU+NkY; _bl_uid=p9k8Idv9lezmvhpeqnw616e9Ipya; ali_apache_track=; ali_apache_tracktmp=; _ga=GA1.2.850805203.1596889391; _gid=GA1.2.77832380.1596889391; XSRF-TOKEN=b5cae2d0-3c92-4c16-b12b-8683107cf5aa; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932913152555; x5sec=7b2261652d676c6f7365617263682d7765623b32223a223030653561353639616337343964343638326637326262306230616339376161434d575a76766b46454a6d6338615458674d6d4552673d3d227d; intl_common_forever=Cl6aEtGrs22121QXfaHaV/be18SJO5bU2J/CEk4MBdjCRlI6JhWbFg==; JSESSIONID=F8674B3780776F56A2F51178032DC8D8; _m_h5_tk=936fb214777faefda4aa2237a32fa6d8_1596951638370; _m_h5_tk_enc=72ccd86403b8c5a1c792f94d641e5ea9; xman_us_f=x_l=0&x_locale=en_US&x_c_chg=0&acs_rt=85f12becf7e848eabaf377b16055e6ef&x_as_i=%7B%22cookieCacheEffectTime%22%3A1596950135646%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D; l=eBxJZ7EnOSKMMZJEBOfahurza77ObIRvXuPzaNbMiOCPOO195TqFBZohbLLpCnGVhsaXR3lil4lwBeYBqCcYIM3IOM87zlMmn; tfstk=cfgOBwis4pvGSsPKacK3hzv26WoOZT5Tn1wAkIxBXK1JXf_AiIuoy0ZkfSWTJBC..; isg=BGZmyL84Bd4potF7GVPZB4I2t9zoR6oBCrH7jFAPTQlk0wbtuNZ8E7ypL8_fsKIZ'''
        req = self.session.get(url, data = data, headers = header, proxies = self.getProxy(), cookies = cookies, timeout = TIME_OUT)

        if req.status_code == 200:
            self.cookies = requests.utils.dict_from_cookiejar(req.cookies)
            return req.text
        else:
            print('request status code : ', req.status_code)
            return ''

    def post(self, url, data = {}, referer = '', cookies = {}):
        """http post request"""
        header = self.getHeader()
        header['Referer'] = referer
        req = self.session.post(url, data = data, headers = header, proxies = self.getProxy(), cookies = cookies, timeout = TIME_OUT)

        if req.status_code == 200:
            return req.text
        else:
            print('request status code : ', req.status_code)
            return ''

    def final(self, url):
        """webdriver loads webpage"""
        options = webdriver.FirefoxOptions()
        options.set_headless()

        proxy = self.getProxy()
        if len(proxy) > 0:
            proxyStr = list(proxy.values())[0]
            proxyList = proxyStr.split(':')
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.http', proxyList[0])
            options.set_preference('network.proxy.http_port', int(proxyList[1]))

        header = self.getHeader()
        if len(header) > 0:
            options.set_preference("general.useragent.override", list(header.values())[0])

        browser = webdriver.Firefox(executable_path = FIREFOX_DRIVER, options = options)
        browser.get(url)
        browser.implicitly_wait(WAIT_TIME)
        content = browser.page_source
        browser.quit()

        return content

    def downloadImg(self, url, fileName, referer = ''):
        """download image"""
        header = self.getHeader()
        header['Referer'] = referer
        req = self.session.get(url, headers = header, proxies = self.getProxy(), timeout = TIME_OUT)

        if req.status_code == 200:
            imgFile = open(fileName, 'wb+')
            imgFile.write(req.content)
            imgFile.close()
        else:
            print('request status code : ', req.status_code)
