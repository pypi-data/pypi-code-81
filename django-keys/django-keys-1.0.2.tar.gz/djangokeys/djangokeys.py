#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains DjangoKeys class.

from os import getenv

from djangokeys.env import read_values_from_env
from djangokeys.exceptions import EnvironmentVariableNotFound
from djangokeys.exceptions import ValueTypeMismatch
from djangokeys.exceptions import ValueIsEmpty


class DjangoKeys:
    """ Used to access values of environment variables that have been set by
        the execution environment, or are listed in an .env file.
    """

    def __init__(self, path):
        """ Initializes a new instance of DjangoKeys.

        :param str path: filepath to .env file containing environment vars

        :raises FileDoesNotExist: specified .env file was not found
        """
        self._path = path
        self._values = read_values_from_env(path)

    def secret_key(self, key, *, overwrite=False):
        """ Access environment variable used to store value of Django's
            SECRET_KEY setting.

        :param str key: name of environment variable
        :param bool overwrite: .env file can overwrite execution environment

        :rtype: str
        :returns: value of environment variable as a string

        :raises EnvironmentVariableNotFound: environment variable not set
        """
        value = self._get_value(key, overwrite=overwrite)
        if value == "":
            msg = "Environment variable '{}' cannot be empty; is secret key."
            raise ValueIsEmpty(msg.format(key))
        else:
            return value

    def str(self, key, *, overwrite=False):
        """ Access environment variable as a simple string.

        :param str key: name of environment variable
        :param bool overwrite: .env file can overwrite execution environment

        :rtype: str
        :returns: value of environment variable as a string

        :raises EnvironmentVariableNotFound: environment variable not set
        """
        return self._get_value(key, overwrite=overwrite)

    def int(self, key, *, overwrite=False):
        """ Access environment variable as an integer.

        :param str key: name of environment variable
        :param bool overwrite: .env file can overwrite execution environment

        :rtype: int
        :returns: value of environment variable as an integer

        :raises EnvironmentVariableNotFound: environment variable not set
        :raises ValueTypeMismatch: value cannot be interpreted as an int
        """
        value = self._get_value(key, overwrite)
        if value == "":
            msg = "Environment variable '{}' is empty; expected int."
            raise ValueIsEmpty(msg.format(key))
        try:
            return int(value)
        except ValueError:
            msg = "Could not interpret environment variable '{}' as int: {}"
            raise ValueTypeMismatch(msg.format(key, value))

    def float(self, key, *, overwrite=False):
        """ Access environment variable as an integer.

        :param str key: name of environment variable
        :param bool overwrite: .env file can overwrite execution environment

        :rtype: int
        :returns: value of environment variable as an integer

        :raises EnvironmentVariableNotFound: environment variable not set
        :raises ValueTypeMismatch: value cannot be interpreted as an int
        """
        value = self._get_value(key, overwrite)
        if value == "":
            msg = "Environment variable '{}' is empty; expected float."
            raise ValueIsEmpty(msg.format(key))
        try:
            return float(value)
        except ValueError:
            msg = "Could not interpret environment variable '{}' as float: {}"
            raise ValueTypeMismatch(msg.format(key, value))

    def bool(self, key, *, overwrite=False):
        """ Access environment variable as a boolean.

        :param str key: name of environment variable
        :param bool overwrite: .env file can overwrite execution environment

        :rtype: bool
        :returns: value of environment variable as an bool

        :raises EnvironmentVariableNotFound: environment variable not set
        :raises ValueTypeMismatch: value cannot be interpreted as a bool
        """
        value = self._get_value(key, overwrite).lower().strip()
        if value == "":
            msg = "Value of environment variable '{}' is empty, expects bool."
            raise ValueIsEmpty(msg.format(key))
        if value in ["f", "false", "0", "n", "no"]:
            return False
        if value in ["t", "true", "1", "y", "yes"]:
            return True
        msg = "Could not interpret environment variable '{}' as bool: {}"
        raise ValueTypeMismatch(msg.format(key, value))

    def _get_value(self, key, overwrite):
        """ Used internally to retrieve value of environment variable.
        """
        oev = getenv(key)
        fev = self._values.get(key, None)
        if oev is None and fev is None:
            msg = "Could not find an environment variable '{}'"
            raise EnvironmentVariableNotFound(msg.format(key))
        elif oev is None:
            return fev
        elif fev is None:
            return oev
        elif overwrite:
            return fev
        else:
            # TODO: "Warning: tried to overwrite environment variable '{}'"
            return oev

    def report_problems(self):
        """ Reports any problems after having been used, such as unused
            environment variables specified in .env file.
        """
        pass  # currently does nothing yet
