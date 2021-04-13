from .tools import is_valid_minecraft_username, is_valid_mojang_uuid

### Main class
class GetPlayerData:
    def __init__(self, identifier, timestamp=None):
        self._mcuuid = None
        self.valid = True

        if is_valid_minecraft_username(identifier):
            self._mcuuid = MCUUID(name=identifier)
        elif is_valid_mojang_uuid(identifier):
            self._mcuuid = MCUUID(uuid=identifier)
        else:
            self.valid = False

        @property
        def uuid(self):
            return self._mcuuid.uuid

        @property
        def username(self):
            return self._mcuuid.name
