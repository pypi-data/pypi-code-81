from AIH_SDK.v1.v1Object import v1Object


class PanoramaImage(v1Object):
    
    def __init__(self):
        super().__init__()
        self._endpoint = 'api/v1/panorama-images'
        
    
    
    def get(self, id:str=None):
        """
        To get a list of all panorama images or a specific panorama image.
        Result is set as self.value
        """
        
        if id:
            self.value = self._client._get(self._api, f'{self._endpoint}/{id}')
            self.value = self.value['panoramaImage']
        else:
            self.value = self._client._get(self._api, self._endpoint)
            self.value = self.value['panoramaImages']
        
        return self
            
    
    
    def post(self):
        """
        To post the updates that have been made to self.value
        """
        
        response_json = self._client._post(self._api, self._endpoint, self.value)
        self.value['id'] = response_json['panoramaImage']['id']
        
        return self