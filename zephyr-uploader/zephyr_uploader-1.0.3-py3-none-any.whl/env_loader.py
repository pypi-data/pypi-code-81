from distutils import util

from .cli_constants import CliConstants
from .environment import EnvironmentSingleton


class EnvLoader:

    def __init__(self):
        self.env = EnvironmentSingleton.get_instance().get_env_and_virtual_env()

    def get_zephyr_config_from_env(self):
        zephyr_config_dict = {}

        if self.env.get(CliConstants.USERNAME.value) is not None:
            zephyr_config_dict[CliConstants.USERNAME.value] = self.env.get(CliConstants.USERNAME.value)

        if self.env.get(CliConstants.PASSWORD.value) is not None:
            zephyr_config_dict[CliConstants.PASSWORD.value] = self.env.get(CliConstants.PASSWORD.value)

        if self.env.get(CliConstants.JIRA_URL.value) is not None:
            zephyr_config_dict[CliConstants.JIRA_URL.value] = self.env.get(CliConstants.JIRA_URL.value)

        if self.env.get(CliConstants.PROJECT_KEY.value) is not None:
            zephyr_config_dict[CliConstants.PROJECT_KEY.value] = self.env.get(CliConstants.PROJECT_KEY.value)

        if self.env.get(CliConstants.RELEASE_VERSION.value) is not None:
            zephyr_config_dict[CliConstants.RELEASE_VERSION.value] = self.env.get(
                CliConstants.RELEASE_VERSION.value)

        if self.env.get(CliConstants.TEST_CYCLE.value) is not None:
            zephyr_config_dict[CliConstants.TEST_CYCLE.value] = self.env.get(CliConstants.TEST_CYCLE.value)

        if self.env.get(CliConstants.REPORT_PATH.value) is not None:
            zephyr_config_dict[CliConstants.REPORT_PATH.value] = self.env.get(CliConstants.REPORT_PATH.value)

        if self.env.get(CliConstants.FOLDER_NAME.value) is not None:
            zephyr_config_dict[CliConstants.FOLDER_NAME.value] = self.env.get(CliConstants.FOLDER_NAME.value)

        if self.env.get(CliConstants.NO_OF_THREADS.value) is not None:
            zephyr_config_dict[CliConstants.NO_OF_THREADS.value] = int(
                self.env.get(CliConstants.NO_OF_THREADS.value))

        if self.env.get(CliConstants.RECREATE_FOLDER.value) is not None:
            zephyr_config_dict[CliConstants.RECREATE_FOLDER.value] = bool(
                util.strtobool(self.env.get(CliConstants.RECREATE_FOLDER.value)))

        if self.env.get(CliConstants.COMMENTS_COLUMN.value) is not None:
            zephyr_config_dict[CliConstants.COMMENTS_COLUMN.value] = int(self.env.get(CliConstants.COMMENTS_COLUMN.value))

        if self.env.get(CliConstants.EXECUTION_STATUS_COLUMN.value) is not None:
            zephyr_config_dict[CliConstants.EXECUTION_STATUS_COLUMN.value] = int(
                self.env.get(CliConstants.EXECUTION_STATUS_COLUMN.value))

        return zephyr_config_dict
