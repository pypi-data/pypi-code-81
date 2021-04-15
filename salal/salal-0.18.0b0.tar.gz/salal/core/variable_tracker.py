from .dependencies import dependencies

class VariableTracker(dict):

    #---------------------------------------------------------------------------
    
    def __init__(self, *args, success_callback, failure_callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_callback = success_callback
        self.failure_callback = failure_callback
        
    #---------------------------------------------------------------------------

    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
            self.success_callback(key)
            return value
        except KeyError:
            self.failure_callback(key)

    #---------------------------------------------------------------------------
