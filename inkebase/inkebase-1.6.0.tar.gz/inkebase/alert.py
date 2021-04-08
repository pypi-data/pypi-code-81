#!/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import socket
import requests

def dingding(access_token, content):
    '''
    推送方式：dingding
    '''
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % (access_token)
    msgtype = 'text'
    values = {
        "msgtype": 'text',
        'text': {
            "content": content
        }
    }
    values = json.dumps(values)
    data = requests.post(url, values,headers=headers)
    errmsg = json.loads(data.text)['errmsg']
    if errmsg == 'ok':
        return "ok"
    return "fail: %s" % data.text


def falcon(metric, value, tag, ctype='GAUGE', step=60, lo_host=socket.gethostname()):
    '''
    推送方式：falcon
    '''
    payload = []
    ts = int(time.time())
    falcon_url = 'http://127.0.0.1:1988/v1/push'
    falcon_dic = {
        "endpoint": lo_host,
        "metric": metric,
        "timestamp": ts,
        "step": step,
        "value": int(value),
        "counterType": ctype,
        "tags": tag
    }
    payload.append(falcon_dic)
    header = {'content-type': "application/json"}
    if len(payload) > 0:
        t = requests.post(falcon_url, data = json.dumps(payload))

if __name__ == '__main__':
    pass


