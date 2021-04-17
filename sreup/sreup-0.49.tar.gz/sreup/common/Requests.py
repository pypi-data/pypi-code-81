import requests
from sreup.common import config


def get(path,retries=3):
    e=0
    rs= None
    while e < retries:
        try:
            rs = requests.get(path).text
            break
        except:
            e += 1
            pass
    return rs
def log(id, log):
    path = config.ServerAdress.REUP_SERVER + "job/log"
    json={
        "id":id,
        "log":log
    }
    rs=requests.post(path, json=json).text
    print(rs)
def result(id,result):
    path = config.ServerAdress.REUP_SERVER + "job/result"
    json = {
        "id": id,
        "result": result
    }
    rs = requests.post(path, json=json).text
    print(rs)
def status(id,status):
    path = config.ServerAdress.REUP_SERVER + "job/status"
    json = {
        "id": id,
        "status": status
    }
    rs = requests.post(path, json=json).text
    print(rs)