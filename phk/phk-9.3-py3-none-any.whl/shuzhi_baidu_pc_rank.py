import requests, time
from copy import deepcopy


class 树枝查百度pc排名():
    headers = {'apikey':''} 
    
    def __init__(self, apikey=''):
        self.headers = deepcopy(self.headers)
        if apikey: self.headers['apikey'] = apikey
        self.tids = {}

    def 推送并存储(self, kw, 关键词字段='kw', 域名字段='domain'):
        tid = self.push_kw(kw[关键词字段], kw[域名字段])
        self.tids[tid] = kw

    def push_kw(self, kw, domain):
        api_url = f'http://query.shuzhikj.com/api/platform/add_task?name={kw}&url={domain}&type=1&urlmode=1'
        r = requests.get(api_url, headers=self.headers)
        return str(int(r.json()['data']))
    
    def tid_get_rank(self, tid):
        api_url = f'http://query.shuzhikj.com/api/platform/get_taskrank?id={tid}'
        rank = requests.get(api_url, headers=self.headers).json()
        if type(rank['data']) is int: return rank['data']
        if rank['msg'] == '查询中': return None
        raise Exception(str(rank['msg']))
    
    def kw_get_rank(self, kw, domain, 最高次数=360, 等待间隔=10):  # 默认1小时
        等待间隔 = 等待间隔 or 0
        tid = self.push_kw(kw, domain)
        i = 0
        while (not 最高次数) or (i < 最高次数):
            i += 1
            rank = self.tid_get_rank(tid)
            if type(rank) is int: return rank
            if (not 最高次数) or (i < 最高次数):
                time.sleep(等待间隔)
        raise Exception("查询失败!")
