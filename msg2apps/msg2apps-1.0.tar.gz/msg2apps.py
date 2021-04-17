import requests
import json
import os


def Wechat(msg, corpid, secret, agentid):
    data = json.dumps({
            "touser" : "admin",
            "msgtype" : "text",
            "agentid" : agentid,
            "text" : {
                "content" : msg
            },
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        })
    url_get_token = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(corpid, secret)
    try:
        token = requests.get(url_get_token, timeout=5).json()["access_token"]
    except Exception as e:
        print(e)
        return
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    try:
        # print(msg)
        r = requests.post(url, data=data, timeout=5)
        print(r.json()['errmsg'])
        return
    except Exception as e:
        print(e)
        return