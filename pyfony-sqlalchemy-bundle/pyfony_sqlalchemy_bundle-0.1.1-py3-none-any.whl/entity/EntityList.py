class EntityList:

    _entities: list

    def __init__(self, entities):
        self._entities = entities

    def __getitem__(self, index):
        return self._entities[index]

    def get_by_id(self, id):
        for entity in self._entities:
            if entity.id == id:
                return entity

        raise None

    def find(self, callback: callable):
        for entity in self._entities:
            if callback(entity):
                return entity

        return None

    def extract(self, callback: callable):
        return EntityList(entity for entity in self._entities if callback(entity))

    def exists(self, callback: callable):
        for entity in self._entities:
            if callback(entity):
                return True

        return False
