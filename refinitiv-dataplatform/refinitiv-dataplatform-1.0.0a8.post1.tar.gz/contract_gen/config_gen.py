import json


class Config(object):
    json_data = {}

    DATA_JSON_FILE_PATH = {}
    INCLUDE = {}
    DO_NOT_DUMP = {}
    ENUM_DUMP_PATH = {}
    MODELS_DUMP_PATH = {}
    IPA_ROOT_DUMP_PATH = {}
    DEFINE_INHERITANCE_EXPLICIT = {}
    INHERITANCE_INSTRUMENT_DEFINITION = {}
    PRIORITY_BY_DATE = {}
    PRIORITY_BY_ARG_NAME = {}
    MODULE_PATH_BY_CLASS_NAME = {}
    RENAME_CLASS = {}
    ENUM_ALIASES = {}
    MODELS = {}

    @classmethod
    def load(cls, config_name):
        with open(config_name) as f:
            cls.json_data = json.loads(f.read())

        cls.DATA_JSON_FILE_PATH = cls.json_data.get('DATA_JSON_FILE_PATH')
        cls.INCLUDE = cls.json_data.get('INCLUDE')
        cls.DO_NOT_DUMP = cls.json_data.get('DO_NOT_DUMP')
        cls.ENUM_DUMP_PATH = cls.json_data.get('ENUM_DUMP_PATH')
        cls.MODELS_DUMP_PATH = cls.json_data.get('MODELS_DUMP_PATH')
        cls.IPA_ROOT_DUMP_PATH = cls.json_data.get('IPA_ROOT_DUMP_PATH')
        cls.DEFINE_INHERITANCE_EXPLICIT = cls.json_data.get('DEFINE_INHERITANCE_EXPLICIT')
        cls.INHERITANCE_INSTRUMENT_DEFINITION = cls.json_data.get('INHERITANCE_INSTRUMENT_DEFINITION')
        cls.PRIORITY_BY_DATE = cls.json_data.get('PRIORITY_BY_DATE')
        cls.PRIORITY_BY_ARG_NAME = cls.json_data.get('PRIORITY_BY_ARG_NAME')
        cls.MODULE_PATH_BY_CLASS_NAME = cls.json_data.get('MODULE_PATH_BY_CLASS_NAME')
        cls.RENAME_CLASS = cls.json_data.get('RENAME_CLASS')
        cls.ENUM_ALIASES = cls.json_data.get('ENUM_ALIASES')
        cls.MODELS = cls.json_data.get('MODELS')
