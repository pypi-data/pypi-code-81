from excel_exporter.excel_exporter.env_constants import EnvConstants
from excel_exporter.excel_exporter.environment import EnvironmentSingleton


class EnvStartupSingleton:
    __instance = None
    __env = EnvironmentSingleton.get_instance()

    @staticmethod
    def get_instance():
        if EnvStartupSingleton.__instance is None:
            EnvStartupSingleton()
        return EnvStartupSingleton.__instance

    def __init__(self):
        if EnvStartupSingleton.__instance is not None:
            raise Exception("This class is a singleton !")
        else:
            EnvStartupSingleton.__instance = self

    def get_config_env_vars(self):
        return {
            EnvConstants.FLUENTD_IP_PORT: self.__env.get_env_and_virtual_env().get(
                EnvConstants.FLUENTD_IP_PORT).strip() if self.__env.get_env_and_virtual_env().get(
                EnvConstants.FLUENTD_IP_PORT) else None
        }
