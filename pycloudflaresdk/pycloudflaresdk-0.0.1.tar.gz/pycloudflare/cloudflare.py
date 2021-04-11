import logging
from itertools import chain
from typing import List, Dict

from .request import HTTP

logger = logging.getLogger(__name__)


class CLOUDFLARE:

    def __init__(self, AuthKey, AuthMail, AccountID):
        self.AccountID = AccountID
        self.http = HTTP(AuthKey, AuthMail)

    def _getDomainList(self, page=1) -> dict:

        return self.http.get(
            url='zones',
            params={'per_page': '50', 'page': page}
        )

    def getDomainList(self) -> List:
        """獲取域名列表

        :return:
        """

        _result = []
        page = 1
        while 1:
            domain = self._getDomainList(page=page)
            if domain['result']:
                _result.append(domain['result'])
                page += 1
            else:
                break

        result = list(chain(*_result))
        return result

    def _createDomain(self, domain="example.com") -> Dict:
        return self.http.post(
            url='zones',
            json={
                "name": domain,
                "account": {"id": self.AccountID},
                "jump_start": True,
                "type": "full"
            }
        )

    def createDomain(self, domain="example.com") -> Dict:
        result = self._createDomain(domain)
        if result['success']:
            logger.debug(result)
            return result
        else:
            # print("\n".join([f"{i['code']} {i['message']}" for i in result['errors']]))
            logger.warning("\n".join([f"{i['code']} {i['message']}" for i in result['errors']]))
            return {}

    def _getDomainRecordList(self, domain_id, page, name=None):
        """
        獲取域名紀錄列表
        :param domain_id:str
        :param match:str
        :return:
        """
        params_data = {"page": page, "per_page": 100}

        if name:
            params_data['name'] = name

        return self.http.get(
            url=f'zones/{domain_id}/dns_records',
            params=params_data
        )

    def getDomainRecordList(self, domain_id, name=None) -> List:
        """

        :param domain_id:
        :param name: str
            abc.example.com
        :return:
        """

        _result = []
        page = 1
        while 1:
            domain = self._getDomainRecordList(domain_id, page, name)
            if domain['result']:
                _result.append(domain['result'])
                page += 1
            else:
                break

        result = list(chain(*_result))
        return result

    def _createDomainRecord(self, domain_id, type, name, content, priority=10, proxied=False, ttl=120):
        """
        新增指定域名紀錄
        """
        return self.http.post(
            url=f'zones/{domain_id}/dns_records',
            json={'type': type, 'name': name, 'content': content, 'ttl': ttl, 'priority': priority, 'proxied': proxied}
        )

    def createDomainRecord(self, domain_id, type, name, content, priority=10, proxied=False, ttl=120):
        result = self._createDomainRecord(domain_id, type, name, content, priority, proxied, ttl)
        if result['success']:
            logger.debug(result)
            return result
        else:
            # print(domain_id, type, name, content, "\n".join([f"{i['code']} {i['message']}" for i in result['errors']]))
            text = "\n".join([f"{i['code']} {i['message']}" for i in result['errors']])
            logger.warning(f"{domain_id} {type} {name} {content} {text}")
            return False

    def _updateDomainRecord(self, domain_id, record_id, type, name, content, ttl=120):
        """更新DNS紀錄
        :param domain_id: str
        :param record_id: str
        :param type: str
        :param name: str
        :param content: str
        :return:
        """
        return self.http.put(
            url=f'zones/{domain_id}/dns_records/{record_id}',
            json={'name': name, 'type': type, 'content': content, 'ttl': ttl}
        )

    def updateDomainRecord(self, domain_id, record_id, type, name, content, ttl=120):
        result = self._updateDomainRecord(domain_id, record_id, type, name, content, ttl)
        if result['success']:
            logger.debug(result)
            return result
        else:
            # print(domain_id, type, name, content, "\n".join([f"{i['code']} {i['message']}" for i in result['errors']]))
            text = "\n".join([f"{i['code']} {i['message']}" for i in result['errors']])
            logger.warning(f"{domain_id} {name} {type} {content} {text}")
            return False

    def deleteDomainRecord(self, domain_id, record_id):
        """刪除DNS紀錄

        :param domain_id:
        :param record_id:
        :return:
        """
        return self.http.delete(
            url=f'zones/{domain_id}/dns_records/{record_id}',
        )
