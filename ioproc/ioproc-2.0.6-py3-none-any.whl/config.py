#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pathlib as pt
import inspect
import pprint

import yaml
import cerberus
import platform

from ioproc.schemas import general_schema, action_schema, checkpoint_schema
from ioproc.logger import mainlogger as log


__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch", "Jan Buschmann"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


class ConfigurationError(Exception):
    """
    Error raised by the configuration process.
    """
    pass


class ConfigDict(dict):

    def __getitem__(self, fieldname):
        """
        Access the config dictionary and retrieve data set by field name.
        If an KeyError is raised and the actionName is None, a ConfigurationError
        is raised, warning the user of an unsuccessful configuration.
        :param field name
        :return data from config dictionary which is accessed using the field name
        """
        try:
            return super().__getitem__(fieldname)
        except KeyError as e:
            s = inspect.stack()

            actionName = None
            lineno = s[0].lineno
            filename = pt.Path(s[0].filename).name

            for idx, iframe in enumerate(s):
                if iframe.function == '__actionwrapper__':
                    last = s[idx - 1]
                    actionName = last.function
                    lineno = last.lineno
                    filename = pt.Path(last.filename).name
                    break

            if actionName is None:
                out = '\n      config field "{}" unavailable\n'\
                      '      in file "{}" in line {}'.format(fieldname, filename, lineno)
            else:
                out = '\n      config field "{}" unavailable\n'\
                      '      requested by action "{}" in line {}\n'\
                      '      in file "{}"'.format(fieldname, actionName, lineno, filename)
            raise ConfigurationError(out)

    def print(self):
        pprint.pprint(self)


class ConfigList(list):
    def __getitem__(self, fieldname):
        """
        Access the config list and retrieve data set by field name.
        If an KeyError is raised and the actionName is None, a ConfigurationError
        is raised, warning the user of an unsuccessful configuration.
        :param field name
        :return data from config list which is accessed using the field name
        """
        try:
            return super().__getitem__(fieldname)
        except (TypeError, IndexError):
            s = inspect.stack()

            actionName = None
            lineno = s[0].lineno
            filename = pt.Path(s[0].filename).name

            for idx, iframe in enumerate(s):
                if iframe.function == '__actionwrapper__':
                    last = s[idx - 1]
                    actionName = last.function
                    lineno = last.lineno
                    filename = pt.Path(last.filename).name
                    break

            if actionName is None:
                out = '\n      element at position {} unavailable\n'\
                      '      in file "{}" in line {}'.format(fieldname, filename, lineno)
            else:
                out = '\n      element at position {} unavailable\n'\
                      '      requested by action "{}" in line {}\n'\
                      '      in file "{}"'.format(fieldname, actionName, lineno, filename)

            raise ConfigurationError(out)


def convertList(d):
    """
    When loading the .yaml, the user defined workflow is stored in a dictionary.
    This method converts the dictionary to a list.
    :return list with actions to execute in workflow
    """
    if not isinstance(d, ConfigDict):
        for ikey, ivalue in d.items():
            if hasattr(ivalue, 'keys'):
                d[ikey] = convertList(ivalue)
            elif not hasattr(ivalue, 'strip') and hasattr(ivalue, '__iter__'):
                d[ikey] = ConfigList(ivalue)
    return d


def loadAndValidate(confPath):
    """
    Loads the config file from a path provided and validates it against a provided schema. If the config file is
    empty, an empty dictionary is returned in order to comply with the following interfaces.
    :param confPath: path to config, schema: validation schema which ensure certain standards of configuration
    :return config dictionary which is validated against a provided schema
    """
    conf = yaml.load(open(confPath), Loader=yaml.Loader)

    if conf is None:
        return {}

    dirs = {}
    if 'directives' in conf:
        dirs = conf['directives']
        del conf['directives']

    validate_config(conf, confPath)

    conf = convertList(conf)

    if isinstance(dirs, list):
        log.warning('DeprecationWarning: `directives` are specified as list. We advice to use dictionaries instead.')
        for idir in dirs:
            for itag, ival in idir.items():
                if itag == 'config':
                    isubConfigTag, isubConfigPath = ival
                    if isubConfigTag in conf:
                        raise KeyError(f'sub config with name "{isubConfigTag}" already exists. Rename subconfig')
                    conf[isubConfigTag] = yaml.load(open(isubConfigPath), Loader=yaml.Loader)

    elif isinstance(dirs, dict):
        for key, file in dirs.items():
            conf[key] = yaml.load(open(file), Loader=yaml.Loader)

    return conf


def validate_config(conf, confPath):
    """
    Raises error when user config violates specified schema. First a 'general_schema' is checked, which assures
    that user.yaml header is set correctly and each action in the workflow is defined with a 'project' and 'call'.
    Then, specified validations for 'call' == 'checkpoint' and all other actions are performed. If any of the
    validations is not successful, the procedure crashes logging the Exception
    """

    v_general = cerberus.Validator(general_schema)
    v_action = cerberus.Validator(action_schema)
    v_checkpoint = cerberus.Validator(checkpoint_schema)

    checks = list()
    validation_violation = list()

    if v_general.validate(conf):
        checks.append(True)

        for item in conf['workflow']:
            wrapped_item = dict()
            wrapped_item['action'] = item

            if list(item.values())[0]['call'] == 'checkpoint':
                if v_checkpoint.validate(wrapped_item):
                    checks.append(True)
                else:
                    checks.append(False)
                    validation_violation.append(v_checkpoint.errors)
            else:
                if v_action.validate(wrapped_item):
                    checks.append(True)
                else:
                    checks.append(False)
                    validation_violation.append(v_action.errors)
    else:
        checks.append(False)
        validation_violation.append(v_general.errors)

    if len(validation_violation) > 0:
        raise ConfigurationError('in config file "{}":\n{}'.format(confPath, validation_violation))


class ConfigProvider:
    """
    The ConfigProvider triggers the reading and validation of the config file.
    For this purpose it sets the pathes, parses the config file for a user schema
    and triggers the validation process.
    """
    def __init__(self):
        self.config = None
        self.userConfigPath = None

    def setPathes(self, userConfigPath):
        self.userConfigPath = userConfigPath

    def parse(self):
        self.config = ConfigDict()
        self.config["user"] = loadAndValidate(self.userConfigPath)

        return self.config

    def get(self):
        if self.config is None:
            self.parse()
        return self.config


configProvider = ConfigProvider()
