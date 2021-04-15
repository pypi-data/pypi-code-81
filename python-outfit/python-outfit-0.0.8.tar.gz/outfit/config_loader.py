import logging
from .utils.logger import Logger, LoggerSetup
from .utils.io import load_yaml

class Outfit(object):
    
    path = None 
    content = None
    
    @staticmethod
    def setup(path):
        Outfit.content = load_yaml(path)
        log_config = Outfit.content['logconfig'] if 'logconfig' in Outfit.content else None

        Logger.mode = 'root'

        if log_config != None:
            mode = log_config['mode'] if 'mode' in log_config else 'root'
            source_type = log_config['source_type'] if 'source_type' in log_config else None
            source_location = log_config['source_location'] if 'source_location' in log_config else None
            default_type = log_config['default_type'] if 'default_type' in log_config else None
            default_location = log_config['default_location'] if 'default_location' in log_config else None

            LoggerSetup.setup_log(mode = mode, source_type = source_type, source_location = source_location,default_type = default_type, default_location = default_location)
        
