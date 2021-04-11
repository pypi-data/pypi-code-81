#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.cli.service.cli_service_impl import CliServiceImpl
from cloudshell.huawei.cli.huawei_cli_handler import HuaweiCli, HuaweiCliHandler

from cloudshell.huawei.wdm.cli.huawei_command_modes import (
    WDMConfigCommandMode,
    WDMEnableCommandMode,
)


class HuaweiWDMCli(HuaweiCli):
    def get_cli_handler(self, resource_config, logger):
        return HuaweiWDMCliHandler(self.cli, resource_config, logger)


class HuaweiWDMCliHandler(HuaweiCliHandler):
    @property
    def default_mode(self):
        return self.modes[WDMEnableCommandMode]

    @property
    def enable_mode(self):
        return self.modes[WDMEnableCommandMode]

    @property
    def config_mode(self):
        return self.modes[WDMConfigCommandMode]

    def _on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs."""
        cli_service = CliServiceImpl(
            session=session, requested_command_mode=self.enable_mode, logger=logger
        )
        cli_service.send_command(
            "screen-length 0 temporary", WDMEnableCommandMode.PROMPT
        )
