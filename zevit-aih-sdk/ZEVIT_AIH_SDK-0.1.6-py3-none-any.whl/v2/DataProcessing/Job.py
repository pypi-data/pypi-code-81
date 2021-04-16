from AIH_SDK.v2.DataProcessing.DataProcessingObject import DataProcessingObject


class Job(DataProcessingObject):
    
    def __init__(self):
        super().__init__()
        self._endpoint = 'Jobs'