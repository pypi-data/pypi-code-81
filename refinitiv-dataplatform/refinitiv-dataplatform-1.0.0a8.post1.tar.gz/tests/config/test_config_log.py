import asyncio
import logging
from importlib import reload

import pytest

import conftest
from refinitiv.dataplatform import configure


@pytest.mark.asyncio
async def test_config_log(write_project_config):
    write_project_config({"config-change-notifications-enabled": True})

    await asyncio.sleep(10)

    reload(configure)

    assert "info" == configure.config.get("logs.level")
    assert configure.config.get("config-change-notifications-enabled")

    session = conftest.open_platform_session()
    level = session.get_log_level()
    assert logging.INFO == level

    write_project_config({"logs": {"level": "INFO"}})

    await asyncio.sleep(10)

    assert "INFO" == configure.config.get("logs.level")

    level = session.get_log_level()
    assert logging.INFO == level
