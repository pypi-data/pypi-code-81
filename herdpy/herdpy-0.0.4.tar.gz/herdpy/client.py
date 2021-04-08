from typing import List, Dict
from requests import Session

class Report:
    url: str
    node_name: str
    group: str = "NOGROUP"
    status_code: str = "OK"
    description: str = "No description given."
    tags: List[str] = []
    severity: int = 5
    ttl: int = 0

    def __init__(self, client: Session):
        self.client = client

    def add_tag(self, tag: str):
        if tag in self.tags:
            return 

        self.tags.append(tag)


    def validate(self) -> None:
        if not self.url:
            raise ValueError("report.url must be set")

        if not self.node_name:
            raise ValueError("Report source or node_name must be set")


    def send(self) -> None:
        self.validate()

        payload: Dict = {
            "id": self.node_name,
            "group": self.group,
            "status_code": self.status_code,
            "description": self.description,
            "severity": self.severity,
            "ttl": self.ttl
        }

        response = self.client.post(url=self.url, json=payload)
        
        if response.status_code == 200:
            return

        raise ConnectionError("Something is wrong")


def new_report() -> Report:
    sess = Session()
    r = Report(sess)
    return r
