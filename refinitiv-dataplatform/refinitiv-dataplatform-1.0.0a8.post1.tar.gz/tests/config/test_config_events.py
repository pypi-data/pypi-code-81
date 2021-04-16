import asyncio
from importlib import reload

import pytest

from refinitiv.dataplatform import configure


@pytest.mark.asyncio
async def test_rewrite_user_config(write_user_config):
    write_user_config({"prop": "value", "config-change-notifications-enabled": True})

    reload(configure)

    assert 'value' == configure.config.get('prop')

    write_user_config('{"prop":"new_value"}')

    await asyncio.sleep(10)

    assert 'new_value' == configure.config.get('prop')


@pytest.mark.asyncio
async def test_rewrite_project_config(write_project_config):
    write_project_config({"prop": "value", "config-change-notifications-enabled": True})

    reload(configure)

    assert 'value' == configure.config.get('prop')

    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(10)

    assert 'new_value' == configure.config.get('prop')


@pytest.mark.asyncio
async def test_update_event(write_project_config):
    fut = asyncio.Future()

    def on_config_updated():
        assert 'new_value' == configure.config.get('prop')
        if not fut.done():
            fut.set_result(1)

    write_project_config('{"prop":"value"}')
    reload(configure)
    configure.config.on('update', on_config_updated)
    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(10)

    await fut


@pytest.mark.asyncio
async def test_update_event(write_project_config):
    def on_config_updated():
        assert False

    write_project_config({"prop": "value", "config-change-notifications-enabled": True})
    reload(configure)
    configure.config.on('update', on_config_updated)
    configure.config.remove_listener('update', on_config_updated)
    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(10)

    assert 'new_value' == configure.config.get('prop')
