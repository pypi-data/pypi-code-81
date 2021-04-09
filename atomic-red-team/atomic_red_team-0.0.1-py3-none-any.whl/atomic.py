import os
import fnmatch

from .utils.exceptions import MissingDefinitionFile

import yaml
import unidecode


class Atomic:

    __path = None
    
    def __init__(self, technique_id: str):
        self.technique_id = technique_id

    def get(self):
        pass

    def get_yaml_file_from_dir(self, path_to_dir):
        """
        Returns path of the first file that matches "*.yaml" in a directory
        """
        for entry in os.listdir(path_to_dir):
            if fnmatch.fnmatch(entry, '*.yaml'):
                # Found the file!
                return os.path.join(path_to_dir, entry)
        raise MissingDefinitionFile("No YAML file describing the technique in {}!".format(path_to_dir))

    def load_technique(self, path_to_dir):
        """
        Loads the YAML content of a technique from its directory. (T*)
        """
        # Load and parses its content.
        # Add logic to identify location of atomics
        with open(self.get_yaml_file_from_dir(path_to_dir), 'r', encoding="utf-8") as f:
            return yaml.load(unidecode.unidecode(f.read()), Loader=yaml.SafeLoader)

