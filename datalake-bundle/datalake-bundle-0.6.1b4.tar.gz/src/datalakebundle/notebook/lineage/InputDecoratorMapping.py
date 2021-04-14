from databricksbundle.notebook.lineage.DecoratorMappingInterface import DecoratorMappingInterface
from datalakebundle.notebook.lineage.DataFrameLoader import DataFrameLoader
from datalakebundle.notebook.lineage.DataFrameSaver import DataFrameSaver
from datalakebundle.notebook.lineage.Transformation import Transformation


class InputDecoratorMapping(DecoratorMappingInterface):
    def get_mapping(self):
        return {
            "transformation": Transformation,
            "data_frame_loader": DataFrameLoader,
            "data_frame_saver": DataFrameSaver,
        }
