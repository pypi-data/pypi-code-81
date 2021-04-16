from enum import Enum


class CliConstants(Enum):
    USERNAME = "username"
    PASSWORD = "password"
    JIRA_URL = "jiraUrl"
    PROJECT_KEY = "projectKey"
    RELEASE_VERSION = "releaseVersion"
    TEST_CYCLE = "testCycle"
    REPORT_PATH = "reportPath"
    NO_OF_THREADS = "noOfThreads"
    RECREATE_FOLDER = "recreateFolder"
    FOLDER_NAME = "folderName"
    COMMENTS_COLUMN = "commentsColumn"
    EXECUTION_STATUS_COLUMN = "executionStatusColumn"
