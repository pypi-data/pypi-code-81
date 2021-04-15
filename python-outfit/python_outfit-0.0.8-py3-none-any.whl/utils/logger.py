import yaml
import os
import logging.config
import logging

modules = ['development', 'production', 'testing']

def load_yaml(path):
    current_path = os.getcwd()
    full_path = ''

    if path[0:2] == './':
        full_path = os.path.join(current_path, path[2:])
    elif path[0:2] == '..':
        full_path = os.path.join(current_path, path)
    else:
        full_path = path

    content = {}
    # get the yaml file
    with open(full_path, 'r') as stream:
        try:
            content = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            logging.error('error load yaml file ' + str(err))

    return content


class LoggerSetup(object):

    @staticmethod
    def load_config_from_yaml_file(source_location = None, default_type = None, default_location = None):

        try:
            log_config = load_yaml(source_location)
            logging.config.dictConfig(log_config)
            
            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return LoggerSetup.source_option(default_type, default_location)

        
    @staticmethod
    def load_config_from_consulkv(source_location = None, default_type = None, default_location = None):

        from ..hashicorp.consul_config import ConsulCon

        try:
            LoggerSetup.consul_con = ConsulCon() if LoggerSetup.consul_con == None else LoggerSetup.consul_con
            LoggerSetup.consul_con.exception_dict['path'] = source_location

            config = LoggerSetup.consul_con.get_kv('yaml')
            logging.config.dictConfig(config)

            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return LoggerSetup.source_option(default_type, default_location)

 

    @staticmethod
    def load_config_from_dict(source_location = None, default_type = None, default_location = None, config_dict = {}):
        try:
            log_config = {} 

            if config_dict == {}:
                import importlib

                temp = importlib.import_module(source_location)
                log_config = temp.logging
            else:
                log_config = config_dict

            logging.config.dictConfig(log_config)
            
            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return LoggerSetup.source_option(default_type, default_location)


    @staticmethod
    def load_config_from_json_file(source_location = None, default_type = None, default_location = None):

        try:
            import json
            with open(source_location, 'rt') as f:
                log_config = json.loads(f.read())
            logging.config.dictConfig(log_config)

            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return LoggerSetup.source_option(default_type, default_location)


    @staticmethod
    def setup_log(mode = 'development', source_type = None, 
                  source_location = None, consul_con = None, config_dict = None,
                  default_type = 'yaml_file', default_location = 'conf/logging.yaml'):
        Logger.update_mode(LoggerSetup.extract_varenv(mode))
        LoggerSetup.consul_con = consul_con
        LoggerSetup.loggers = LoggerSetup.source_option(source_type, source_location, default_type, default_location)
        if Logger.mode not in LoggerSetup.loggers:
            raise Exception('modules for mode '+ Logger.mode +' is not found!!') 

    @staticmethod
    def extract_varenv(v):
        value = str(v) if type(v) == int else v

        def check_envvar(val):
            return os.environ[val] if val in os.environ else None
        # checking if the string of value is in environment variables
        temp = check_envvar(v[2:len(v)-1]) if ('${' == value[0:2]) and ('}' == value[len(value)-1]) else v
        if temp == None:
            raise Exception('var value {0}  not found'.format(value))
        return temp

     
    @staticmethod
    def source_option(source_type = None, source_location = None, default_type = None, default_location = None):

        source_type = LoggerSetup.extract_varenv(source_type)
        source_location = LoggerSetup.extract_varenv(source_location)
        default_type = LoggerSetup.extract_varenv(default_type)
        default_location = LoggerSetup.extract_varenv(default_location)
        mode_enum = {
            'yaml_file' : lambda x, y, z: LoggerSetup.load_config_from_yaml_file(x, y, z),
            'consulkv' : lambda x, y, z: LoggerSetup.load_config_from_consulkv(x, y, z),
            'dictionary' : lambda x, y, z: LoggerSetup.load_config_from_dict(x, y, z),
            'json_file' : lambda x, y, z: LoggerSetup.load_config_from_json_file(x, y, z)
        }
        return mode_enum[source_type](source_location, default_type, default_location)

 
class Logger(object):
    mode = 'development'
    consul_con = None 
    loggers = []
    info = logging.getLogger(mode).info
    debug = logging.getLogger(mode).debug
    error = logging.getLogger(mode).error
    critical = logging.getLogger(mode).critical
    exception = logging.getLogger(mode).exception

    @staticmethod
    def update_mode(mode = 'development'):
        Logger.mode = mode
        Logger.info = logging.getLogger(mode).info
        Logger.debug = logging.getLogger(mode).debug
        Logger.error = logging.getLogger(mode).error
        Logger.critical = logging.getLogger(mode).critical
        Logger.exception = logging.getLogger(mode).exception


