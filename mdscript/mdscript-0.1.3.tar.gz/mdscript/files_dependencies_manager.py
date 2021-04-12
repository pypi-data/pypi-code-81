from mdscript.watcher import Watcher
from typing import Set, Dict


class FilesDependenciesManager:
    def __init__(self, watcher: Watcher):
        self.watcher = watcher
        self._parents_to_dependencies: Dict[str, Set[str]] = dict()
        self._dependencies_to_parents: Dict[str, Set[str]] = dict()

    @property
    def parents_to_dependencies(self):
        return self._parents_to_dependencies

    @property
    def dependencies_to_parents(self):
        return self._dependencies_to_parents

    def add_dependency(self, parent_filepath: str, dependency_path: str):
        if parent_filepath not in self._parents_to_dependencies:
            self._parents_to_dependencies[parent_filepath] = {dependency_path}
        else:
            self._parents_to_dependencies[parent_filepath].add(dependency_path)

        if dependency_path not in self._dependencies_to_parents:
            self._dependencies_to_parents[dependency_path] = {parent_filepath}
        else:
            self._dependencies_to_parents[dependency_path].add(parent_filepath)

        self.watcher.add_file_watch(filepath=dependency_path)

