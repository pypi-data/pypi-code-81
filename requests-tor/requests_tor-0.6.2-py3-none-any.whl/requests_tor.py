from time import sleep
from random import choice
from itertools import cycle
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests
from stem import Signal
from stem.control import Controller


class RequestsTor():
    """
    tor_ports = specify Tor socks ports tuple (default is (9150,), as the default in Tor Browser),
    if more than one port is set, the requests will be sent sequentially through the each port;
    tor_cport = specify Tor control port (default is 9151 for Tor Browser, for Tor use 9051);
    password = specify Tor control port password (default is None);
    autochange_id = number of requests via a one Tor socks port (default=5) to change TOR identity.
    threads = specify threads to download urls list (default=8),
    """

    def __init__(
        self,
        tor_ports=(9150,),
        tor_cport=9151,
        password=None,
        autochange_id=5,
        threads=8,
    ):
        self.tor_ports = tor_ports
        self.tor_cport = tor_cport
        self.password = password
        self.autochange_id = autochange_id
        self.threads = threads
        self.ports = cycle(tor_ports)
        self.newid_counter = autochange_id * len(tor_ports)
        self.newid_cycle = (
            cycle(range(1, autochange_id * len(tor_ports) + 1))
            if autochange_id
            else None
        )
        self.ip_api = (
            "https://api.my-ip.io/ip",
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ipinfo.io/ip",
            "https://wtfismyip.com/text",
            "https://ifconfig.me/ip",
            "https://checkip.amazonaws.com",
            "https://ip.seeip.org",
            "https://bot.whatismyipaddress.com",
            "https://api.myip.la",
        )

    def new_id(self, debug=0):
        with Controller.from_port(port=self.tor_cport) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
            if debug == 1:
                print(f"\ntor_cport authenticated: {controller.is_authenticated()}")
            print("TOR NEW IDENTITY SIGNAL. Sleep 3 sec.\n")
            sleep(3)

    def check_ip(self):
        my_ip = self.get(choice(self.ip_api)).text
        print(f"my_ip = {my_ip}")
        return my_ip

    def get(self, url, **kwargs):
        tor_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        }
        port = next(self.ports)
        proxies = {
            "http": f"socks5h://localhost:{port}",
            "https": f"socks5h://localhost:{port}",
        }
        kwargs["headers"] = kwargs.get("headers", tor_headers)
        resp = requests.get(url, **kwargs, proxies=proxies)
        print(f"SocksPort={port} status={resp.status_code} url={resp.url}")
        if self.autochange_id and next(self.newid_cycle) == self.newid_counter:
            self.new_id()
        return resp

    def get_urls(self, urls, **kwargs):
        results, temp_urls = [], []
        step = self.newid_counter
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for i, url in enumerate(urls, start=1):
                temp_urls.append(url)
                if i % step == 0:
                    temp_results = [
                        resp
                        for resp in executor.map(partial(self.get, **kwargs), temp_urls)
                    ]
                    results.extend(temp_results)
                    temp_urls.clear()
                    print(f"Progress: {i} urls")
                    sleep(3)
            temp_results = [
                resp for resp in executor.map(partial(self.get, **kwargs), temp_urls)
            ]
            results.extend(temp_results)
            print("Progress: finished")
        return results

    def test(self):
        print("\n******************TOR NEW ID test******************\n")
        self.new_id(debug=1)
        
        print("\n******************HEADERS test******************\n")
        check_anything = self.get("https://httpbin.org/anything")
        print(check_anything.text)
        
        print("\n******************One thread test******************\n")
        print(f"Socks ports = {self.tor_ports}. Autochange_id = {self.autochange_id}")
        ip_url = choice(self.ip_api)
        print(f"Checking your ip from: {ip_url}")
        for _ in range(min(len(self.tor_ports) * self.autochange_id * 2, 20)):
            resp = self.get(ip_url)
            print(f"my ip = {resp.text}")
            
        print("\n******************Multithreading test******************\n")
        ip_url = choice(self.ip_api)
        print(f"Checking your ip from: {ip_url}")
        my_ip_list = [ip_url for _ in range(min(len(self.tor_ports) * self.autochange_id * 4, 40))]
        results = self.get_urls(my_ip_list)
        results_counter = Counter(res.text for res in results)
        print("\nResults:")
        for k, item in results_counter.items():
            print(f"Your IP: {k} was {item} times")
