#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.service.command_mode import CommandMode
from cloudshell.huawei.cli.huawei_command_modes import (
    ConfigCommandMode,
    EnableCommandMode,
)


class WDMEnableCommandMode(EnableCommandMode):
    pass


class WDMConfigCommandMode(ConfigCommandMode):
    ENTER_COMMAND = "system-view immediately"


CommandMode.RELATIONS_DICT = {EnableCommandMode: {ConfigCommandMode: {}}}
