from abc import ABC
from sqlalchemy import update
from pprint import pprint

class AbstractApplication(ABC):

    """ Abstract Class responsible for implemeting functions that are common in a Application. """ 

    def __init__(self, service):
        self.service = service

    def find_all (self):
        return self.service.find_all()

    def create(self, object):
        return self.service.create (object)

    def update (self, object):
        self.service.update(object)

    def find_by_name (self, name):
        return self.service.find_by_name(name)

    def find_by_uuid (self, uuid):
        return self.service.find_by_uuid(uuid)

