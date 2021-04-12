from AIH_SDK.v2.Assets.AssetsObject import AssetsObject


class MainSystem(AssetsObject):
    
    def __init__(self):
        super().__init__()
        self._endpoint = 'mainsystems'
    
    
