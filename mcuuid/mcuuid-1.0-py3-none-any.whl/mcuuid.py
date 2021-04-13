from .tools import is_valid_minecraft_username, is_valid_mojang_uuid

import json
import requests

class MCUUID:
    def __init__(self, name = None, uuid = None):
        assert not((name == None and uuid == None) or (name != None and uuid != None))
        self._name = name
        self._uuid = uuid
        self._pretty_name = None
        self._names = None

    @property
    def uuid(self):
        self._load_by_name()
        return self._uuid

    @property
    def name(self):
        if self._pretty_name == None:
            if self._name == None:
                self._load_by_uuid()
            else:
                self._load_by_name()
        return self._pretty_name

    @property
    def names(self):
        if self._uuid == None:
            self._load_by_name()
        self._load_by_uuid()
        return self._names

    def _load_by_name(self):
        if self._uuid == None:
            r = requests.get("https://api.mojang.com/users/profiles/minecraft/{name}".format(
                name=self._name,
            ), headers = {
                'Content-Type':'application/json',
            })
            data = json.loads(r.text)
            self._uuid = data["id"]
            self._pretty_name = data["name"]

    def _load_by_uuid(self):
        if self._names == None:
            r = requests.get("https://api.mojang.com/user/profiles/{uuid}/names".format(
                uuid=self._uuid,
            ), headers = {
                'Content-Type':'application/json',
            })
            data = json.loads(r.text)
            self._names = {d.get("changedToAt", 0): d.get("name") for d in data}
            self._pretty_name = self._names.get(max(self._names.keys()))
