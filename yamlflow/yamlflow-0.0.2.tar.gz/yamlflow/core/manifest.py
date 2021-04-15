import sys

import yaml

class Manifest:

    def __init__(self, yaml_file: str):
        super().__init__()
        self._yf = yaml_file
        self._read()

    
    def _read(self) -> None:
        with open(self._yf, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                sys.exit(exc) #NOTE: status code

    def validate(self) -> bool:
        return True


    def build(self):
        pass
