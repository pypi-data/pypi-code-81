from databricksbundle.notebook.lineage.DecoratorMappingInterface import DecoratorMappingInterface
from databricksbundle.notebook.lineage.NotebookFunction import NotebookFunction


class InputDecoratorMapping(DecoratorMappingInterface):
    def get_mapping(self):
        return {
            "notebook_function": NotebookFunction,
        }
