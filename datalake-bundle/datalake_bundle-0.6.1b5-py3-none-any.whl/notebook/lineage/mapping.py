from datalakebundle.notebook.lineage.DataFrameLoader import DataFrameLoader
from datalakebundle.notebook.lineage.DataFrameSaver import DataFrameSaver
from datalakebundle.notebook.lineage.Transformation import Transformation


def get_mapping():
    return {
        "transformation": Transformation,
        "data_frame_loader": DataFrameLoader,
        "data_frame_saver": DataFrameSaver,
    }
