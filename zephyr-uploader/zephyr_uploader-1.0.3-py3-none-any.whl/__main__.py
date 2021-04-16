#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

import pyexcel

from zephyr_uploader.zephyr_uploader.env_loader import EnvLoader
from .zephyr_service import ZephyrService
from .zephyr_uploader import ZephyrUploader
from zephyr_uploader.zephyr_uploader.exit_constants import ExitConstants
from zephyr_uploader.zephyr_uploader.zephyr_config import ZephyrConfigurer
from zephyr_uploader.zephyr_uploader.cli_constants import CliConstants


@click.command()
@click.option('--username', help='The username used to log in Jira. E.g. auto-robot')
@click.option('--password', help='The password used to log in Jira. E.g. passw0rd123!')
@click.option('--jira_url', help='The jira url REST endpoint used to submit the results, including the last /. '
                                 'E.g. http://jira.yourcompany.com/rest/')
@click.option('--project_key', help='The project key in Jira. E.g. AIP')
@click.option('--release_version', help='The release version. E.g. 1.2-UP2020-4')
@click.option('--test_cycle', help='The test cycle. E.g. Regression_Automated')
@click.option('--report_path', help='The Excel report path on the disk. E.g. Results.xls')
@click.option('--no_of_threads', default=10,
              help='The number of threads to be used to upload the test executions. E.g. 10')
@click.option('--recreate_folder', default=False, help='Recreate the folder under the test cycle or not. '
                                                       'E.g. true. Default: false')
@click.option('--folder_name', help='The release version. E.g. centos7-mysql8-SNAPSHOT. Default: default')
@click.option('--execution_status_column', default=6, help='The execution status column which contains the keywords '
                                                           'SUCCESS/FAILURE. E.g. 10. Default: 6')
@click.option('--comments_column', default=8,
              help='The comments column, for example the link log the logs for the test.'
                   ' E.g. 11. Default: 8')
def cli(username, password, jira_url, project_key, release_version, test_cycle, report_path, no_of_threads,
        recreate_folder, folder_name, execution_status_column, comments_column):
    zephyr_config_dict = EnvLoader().get_zephyr_config_from_env()
    zephyr_configurer = ZephyrConfigurer(zephyr_config_dict)

    zephyr_config_cli = {
        CliConstants.USERNAME.value: username,
        CliConstants.PASSWORD.value: password,
        CliConstants.JIRA_URL.value: jira_url,
        CliConstants.TEST_CYCLE.value: test_cycle,
        CliConstants.PROJECT_KEY.value: project_key,
        CliConstants.RELEASE_VERSION.value: release_version,
        CliConstants.REPORT_PATH.value: report_path,
        CliConstants.FOLDER_NAME.value: folder_name,
        CliConstants.NO_OF_THREADS.value: no_of_threads,
        CliConstants.RECREATE_FOLDER.value: recreate_folder,
        CliConstants.COMMENTS_COLUMN.value: comments_column,
        CliConstants.EXECUTION_STATUS_COLUMN.value: execution_status_column
    }

    zephyr_configurer.override_or_set_default(zephyr_config_cli)
    zephyr_configurer.validate()

    try:
        sheet = pyexcel.get_sheet(file_name=zephyr_configurer.get_config().get(CliConstants.REPORT_PATH.value))
        excel_data = sheet.to_array()
        zephyr_uploader = ZephyrUploader(ZephyrService(zephyr_configurer=zephyr_configurer))
        zephyr_uploader.upload_jira_zephyr(excel_data=excel_data)
    except Exception as e:
        click.echo(e.__str__())
        exit(ExitConstants.FAILURE.value)

    exit(ExitConstants.SUCCESS.value)


if __name__ == "__main__":
    cli()
