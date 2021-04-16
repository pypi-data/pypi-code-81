"""Upload test executions in Jira Zephyr
Import the `ZephyrUploader` class to upload zephyr test executions:
    >>> from zephyr_uploader.zephyr_uploader import ZephyrUploader
    >>> from zephyr_uploader.zephyr_service import ZephyrService
    >>> from zephyr_uploader.model.zephyr_config_dict import ZephyrConfigurer
    >>> config_dict = {
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
    >>> # config_dict = EnvLoader().get_zephyr_config_from_env() # in case a file 'environment.properties is used
    >>> zephyr_configurer = ZephyrConfigurer(config_dict)
    >>> zephyr_configurer.validate()
    >>> zephyr_service = ZephyrService(zephyr_configurer=zephyr_configurer)
    >>> zephyr_uploader = ZephyrUploader(zephyr_service)
    >>> sheet = pyexcel.get_sheet(file_name=zephyr_configurer.get_config().get(CliConstants.REPORT_PATH.value))
    >>>    excel_data = sheet.to_array()
    >>> zephyr_uploader.upload_jira_zephyr(excel_data=excel_data)

See https://github.com/estuaryoss/test-libs-python/tree/master/zephyr_uploader for more information
"""
