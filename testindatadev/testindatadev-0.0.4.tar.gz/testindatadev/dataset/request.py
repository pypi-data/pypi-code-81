import sys
import os
import requests
import json

sys.path.append(os.path.dirname(__file__) + os.sep + '../')


class Request:
    def __init__(self, T_key, dataset_id, ip):
        self.T_key = T_key
        self.dataset_id = dataset_id
        self.ip = ""
        if ip:
            self.ip = ip
            self.API_ADDRESS_PREFIX = f"http://{self.ip}/api/v1/"
        else:
            self.API_ADDRESS_PREFIX = "http://127.0.0.1/api/v1/"

    def RiseException(self, response_text):
        raise Exception("error msg from server: " + response_text)

    def GetAccess(self):
        api = f'{self.API_ADDRESS_PREFIX}dataset/{self.dataset_id}/getosskey'
        headers = {"T-Key":self.T_key}
        res = requests.request("GET", api, headers=headers)
        resData = json.loads(res.text)
        if resData['code'] != "":
            self.RiseException(res.text)

        ret = {
            "access_key":resData["data"]["access_key"],
            "secret_key":resData["data"]["access_token"],
            "endpoint":resData["data"]["endpoint"],
            "bucket":resData["data"]["bucket"],
            "type":resData["data"]["type"],
        }

        return ret

    def Upload(self, data):
        api = f'{self.API_ADDRESS_PREFIX}dataset/{self.dataset_id}/upload'
        headers = {"T-Key": self.T_key, "Content-Type":"application/json"}

        res = requests.post(api, headers=headers, data=json.dumps(data))
        resData = json.loads(res.text)
        if resData['code'] != "":
            self.RiseException(res.text)

        ret = {
            "succ": resData["data"]["succ"],
            "fail": resData["data"]["fail"],
        }

        return ret

    def Delete(self, referId):
        api = f'{self.API_ADDRESS_PREFIX}dataset/{self.dataset_id}/refloc/{referId}'
        headers = {"T-Key": self.T_key, "Content-Type": "application/json"}
        res = requests.delete(api, headers=headers)
        resData = json.loads(res.text)
        if resData['code'] != "":
            self.RiseException(res.text)

        ret = {
            "succ": resData["data"]["succ"],
            "fail": resData["data"]["fail"],
        }

        return ret

    def GetData(self, offset, limit):
        api = f'{self.API_ADDRESS_PREFIX}dataset/{self.dataset_id}/data'
        headers = {"T-Key": self.T_key, "Content-Type": "application/json"}
        res = requests.post(api, headers=headers, data=json.dumps({"offset":offset, "limit":limit}))
        resData = json.loads(res.text)
        if resData['code'] != "":
            self.RiseException(res.text)


        return resData["data"]
