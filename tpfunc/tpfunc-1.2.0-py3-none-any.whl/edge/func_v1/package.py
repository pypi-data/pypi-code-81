#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json


class Configuration():
    """
    The configuration object used by default in function
    """
    def __init__(self):
        self.__load_configuration()
        self.__load_trigger_time()

    def __load_configuration(self):
        try:
            cwd = os.getcwd()
            config = os.getenv('CONFIG')
            config = (cwd + '/package.json') if config is None else config
            with open(config, "r") as f:
                self._db  = json.load(f)
        except Exception as e:
            self.__load_default()

    def __load_default(self):
        self._db = {}
        self._db['executable'] = {}
        self._db['trigger'] = {}
        self._db['expose'] = {}
        self._db['params'] = {}

    def __load_trigger_time(self):
        data = os.getenv('DATA')
        self.__trigger_time = data if data else ""

    def data_driven_tags(self):
        """The target tags that will trigger your function up.
        """
        trigger = self._db['trigger'].get('dataDriven', None)
        if trigger is None:
            return {}
        return trigger.get('tags', {})

    def data_driven_events(self):
        """The target events that will trigger your function up.
        """
        trigger = self._db['trigger'].get('dataDriven', None)
        if trigger is None:
            return {}
        return trigger.get('events', {})

    def name(self):
        """The name of your function package.

        Returns:
            name (string)
        """
        return self._db.get('name', '')

    def expose_tags(self):
        """The virtual tags created/destoried by default as
            your function up/down.
        """
        return self._db['expose'].get('tags', [])

    def parameters(self):
        """The pre-defined parameters of your function package.

        Returns:
            A dict mapping keys to the corresponding table of parameters.

            example:
            {'version': '1.0.0', 'arch': 'amd64'}
        """
        return self._db.get('params', {})

    def boot_time(self):
        """The start time of your function.
        """
        return self.__trigger_time
