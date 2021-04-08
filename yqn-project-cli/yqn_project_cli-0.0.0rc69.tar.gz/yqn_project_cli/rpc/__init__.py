# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import abc


class RPCConfigBase(metaclass=abc.ABCMeta):
    def __init__(self, client_config=None, use_conf_management=False, project_config=None,
                 server_manager=None, **kwargs):
        assert client_config is not None or use_conf_management is True, 'client_config or use_conf_management ?!'

        assert not (server_manager is None and use_conf_management), "server_manager doesn't existed yet"

        self.client_config = client_config  # local client config from environ or file
        self.use_conf_management = use_conf_management  # use server config management or not
        self.project_config = project_config  # know project config info from from master or not
        self.server_manager = server_manager  # server conf manager like apollo

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.connector = None

    @abc.abstractmethod
    def connect(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def reconnect(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def close(self, **kwargs):
        raise NotImplementedError
