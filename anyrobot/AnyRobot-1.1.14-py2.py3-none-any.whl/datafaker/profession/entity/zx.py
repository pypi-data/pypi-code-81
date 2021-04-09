import jsonpath
import requests,json
from aishu import setting
from aishu.datafaker.profession.entity import id
from aishu.datafaker.profession.entity import name,timestamp,zx

class search(object):
    def createSearchId(self):
        url = "http://{ip}/v1/search/submit".format(ip=setting.host)
        logGroup = id.date().getDefaultLogGroupID()
        payload = [
            {
                "logGroup": logGroup,
                "query": "*",
                "sort": [
                    {
                        "@timestamp": "desc"
                    }
                ],
                "size": 10,
                "needFieldList": True,
                "filters": {
                    "must": [
                        {
                            "@timestamp": {
                                "from": 1441001644796,
                                "to": 1598854444796
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        ]
        headers = setting.header

        rsp = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        s_id = jsonpath.jsonpath(rsp.json(), '$..{name}'.format(name='id'))
        if isinstance(s_id,bool):
            return False
        else:
            return s_id[0]

    def createInspectionID(self):
        url = "http://{ip}/manager/inspections/inspection".format(ip=setting.host)
        assigned = id.date().getAdminID()
        number = name.date().getName()
        time = timestamp.date().getStartTime()
        payload = {
                "assign": assigned,
                "name": number,
                "info": "This is a test case by AT",
                "ctime": time
        }
        headers = setting.header

        rsp = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        InspectionID = jsonpath.jsonpath(rsp.json(), '$..{name}'.format(name='id'))
        if isinstance(InspectionID,bool):
            return False
        else:
            return InspectionID[0]

    def createInspectionTaskID(self):
        url = "http://{ip}/manager/inspections/task".format(ip=setting.host)
        InspectionID = zx.search().createInspectionID()
        number = name.date().getName()
        payload = {

                "name": number,
                "position": "localUpload",
                "info": "step one: find the target page ；step two：write the check result",
                "inspectionID": InspectionID
        }
        headers = setting.header

        rsp = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        InspectionTaskID = jsonpath.jsonpath(rsp.json(), '$..{name}'.format(name='id'))
        if isinstance(InspectionTaskID,bool):
            return False
        else:
            return InspectionTaskID[0]

if __name__ == '__main__':
    setting.host = "192.168.84.85"
    setting.database = 'AnyRobot'
    setting.password = 'eisoo.com'
    setting.port = 30006
    setting.user = 'root'
    date = search().createInspectionTaskID()
    print(date)