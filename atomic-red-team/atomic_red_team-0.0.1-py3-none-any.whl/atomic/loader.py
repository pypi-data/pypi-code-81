import os
import logging
from pathlib import Path

import yaml

__LOGGER__ = logging.getLogger(__name__)


class Loader:

    __techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'

    def __get_file_name(self, path):
        return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1].split('.')[0]

    def get_self_path(self):
        return os.path.dirname(os.path.abspath(__file__))

    def find_atomics(self, path, pattern='atomics/T*/T*.yaml'):
        result = []
        for path in Path(path).rglob(pattern):
            result.append(os.path.abspath(path))
        return result

    def load_technique(self, path_to_dir):
        with open(path_to_dir, 'r', encoding="utf-8") as f:
            return yaml.load(f.read(), Loader=yaml.SafeLoader)

    def load_techniques(self, atomics_path):
        if not os.path.exists(os.path.abspath(atomics_path)):
            atomics_path = self.find_atomics(self.get_self_path())
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')
        else:
            atomics_path = self.find_atomics(atomics_path)
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')

        for atomic_entry in atomics_path:
            technique = self.__get_file_name(atomic_entry)
            if not self.__techniques.get(technique):
                self.__techniques[technique] = self.load_technique(atomic_entry)
        return self.__techniques
