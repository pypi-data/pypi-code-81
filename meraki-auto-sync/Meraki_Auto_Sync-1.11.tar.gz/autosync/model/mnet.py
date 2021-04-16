from autosync import Products

class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)
class MNET(object):
    #Network Object for each dashboard network
    def __init__(self,net):
        self.id = net['id']
        self.orgId = net['organizationId']
        self.name = net['name']
        self.tags = net['tags']
        self.products = net['productTypes']
        self.syncruntime = None
        self.lastsync = None
        self.cached = False
        self.supported = Products.supported
        self.dashboard = self._getConfig()
        self.functions = self._product_functions()
    def _getConfig(self):
        List = {}
        for product in self.supported:
            tmethod = getattr(Products, product)
            method = getattr(tmethod,product)
            temp = method()
            t = {product: temp}
            List.update(t)
        return List
    def _product_functions(self):
        List = {}
        for product in self.supported:
            #method = getattr(self,dashboard[product])
            _module = dir(self.dashboard[product])
            update = [_funct.split('_')[1] for _funct in _module if
                                  _funct.startswith('Update_')]
            get = [_funct.split('_')[1] for _funct in _module if
                               _funct.startswith('Get_')]
            t = {product:{'update': update, 'get': get}}
            List.update(t)
        return List
        
    def __dir__(self):
        return self.__dict__.keys()

