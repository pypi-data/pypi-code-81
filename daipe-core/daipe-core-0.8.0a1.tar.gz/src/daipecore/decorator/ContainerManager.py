import os
from injecta.container.ContainerInterface import ContainerInterface
from daipecore.DaipeCore import DaipeCore


class ContainerManager:

    _container: ContainerInterface

    @classmethod
    def set_container(cls, container: ContainerInterface):
        cls._container = container

    @classmethod
    def get_container(cls):
        if not hasattr(cls, "_container"):
            cls._container = cls._create_container()

        return cls._container

    @staticmethod
    def _create_container():
        bootstrap_config = DaipeCore.config_reader()
        return bootstrap_config.container_init_function(os.environ["APP_ENV"], bootstrap_config)
