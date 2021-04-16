import pickledb
from lazy import lazy


class PickledbAdapter(object):

    @lazy
    def db(self):
        return pickledb.load(self._config.storage_location(), auto_dump=False)

    def __init__(self, c) -> None:
        self._config = c

    def set(self, key, data, is_dump=True):
        self.db.set(key, data)
        is_dump and self.db.dump()

    def set_list(self, l):
        for d in l:
            self.set(d.get('key'), d.get('data'), False)
        self.db.dump()

    def get(self, key):
        return self.db.get(key)

    def get_list(self, key):
        if not self.db.exists(key):
            self.db.lcreate(key)
        return self.get(key)

    def getall(self):
        return self.db.getall()

    def dump(self):
        return self.db.dump()
