from unittest import TestCase

from .cli_constants import CliConstants


class ZephyrConfigurer(TestCase):
    def __init__(self, zephyr_config_dict={}):
        """
        The config is a dict with all the details
        """
        self.zephyr_config_dict = zephyr_config_dict

    def validate(self):
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.USERNAME.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.PASSWORD.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.JIRA_URL.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.TEST_CYCLE.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.PROJECT_KEY.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.RELEASE_VERSION.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.REPORT_PATH.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.FOLDER_NAME.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.NO_OF_THREADS.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.RECREATE_FOLDER.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.COMMENTS_COLUMN.value), None)
        self.assertIsNot(self.zephyr_config_dict.get(CliConstants.EXECUTION_STATUS_COLUMN.value), None)

    def get_config(self):
        return self.zephyr_config_dict

    def set_config(self, zephyr_config_dict):
        self.zephyr_config_dict = zephyr_config_dict

    def override_or_set_default(self, zephyr_config_dict):
        if zephyr_config_dict.get(CliConstants.USERNAME.value) is not None:
            self.zephyr_config_dict[CliConstants.USERNAME.value] = zephyr_config_dict.get(CliConstants.USERNAME.value)
        if zephyr_config_dict.get(CliConstants.PASSWORD.value) is not None:
            self.zephyr_config_dict[CliConstants.PASSWORD.value] = zephyr_config_dict.get(CliConstants.PASSWORD.value)
        if zephyr_config_dict.get(CliConstants.JIRA_URL.value) is not None:
            self.zephyr_config_dict[CliConstants.JIRA_URL.value] = zephyr_config_dict.get(CliConstants.JIRA_URL.value)
        if zephyr_config_dict.get(CliConstants.TEST_CYCLE.value) is not None:
            self.zephyr_config_dict[CliConstants.TEST_CYCLE.value] = zephyr_config_dict.get(
                CliConstants.TEST_CYCLE.value)
        if zephyr_config_dict.get(CliConstants.PROJECT_KEY.value) is not None:
            self.zephyr_config_dict[CliConstants.PROJECT_KEY.value] = zephyr_config_dict.get(
                CliConstants.PROJECT_KEY.value)
        if zephyr_config_dict.get(CliConstants.RELEASE_VERSION.value) is not None:
            self.zephyr_config_dict[CliConstants.RELEASE_VERSION.value] = zephyr_config_dict.get(
                CliConstants.RELEASE_VERSION.value)
        if zephyr_config_dict.get(CliConstants.REPORT_PATH.value) is not None:
            self.zephyr_config_dict[CliConstants.REPORT_PATH.value] = zephyr_config_dict.get(
                CliConstants.REPORT_PATH.value)
        if zephyr_config_dict.get(CliConstants.FOLDER_NAME.value) is not None:
            self.zephyr_config_dict[CliConstants.FOLDER_NAME.value] = zephyr_config_dict.get(
                CliConstants.FOLDER_NAME.value)
        self.zephyr_config_dict[CliConstants.NO_OF_THREADS.value] = zephyr_config_dict.get(
            CliConstants.NO_OF_THREADS.value) if \
            self.zephyr_config_dict.get(CliConstants.NO_OF_THREADS.value) is not None else 10
        self.zephyr_config_dict[CliConstants.RECREATE_FOLDER.value] = zephyr_config_dict.get(
            CliConstants.RECREATE_FOLDER.value) if \
            self.zephyr_config_dict.get(CliConstants.RECREATE_FOLDER.value) is not None else False
        self.zephyr_config_dict[CliConstants.EXECUTION_STATUS_COLUMN.value] = zephyr_config_dict.get(
            CliConstants.EXECUTION_STATUS_COLUMN.value) if \
            self.zephyr_config_dict.get(CliConstants.EXECUTION_STATUS_COLUMN.value) is not None else 6
        self.zephyr_config_dict[CliConstants.COMMENTS_COLUMN.value] = zephyr_config_dict.get(
            CliConstants.COMMENTS_COLUMN.value) if \
            self.zephyr_config_dict.get(CliConstants.COMMENTS_COLUMN.value) is not None else 8
