# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

from configupdater import ConfigUpdater
from configparser import ConfigParser
import os
import pkg_resources

ini_path = (
    os.path.join("/", "etc", "digital-hydrant", "config.ini")
    if not "DH_CONFIG" in os.environ
    else os.environ.get("DH_CONFIG")
)
default_ini_path = pkg_resources.resource_filename(
    "digital_hydrant", "config/config.ini"
)
db_path = (
    os.path.join("/", "var", "lib", "digital-hydrant", "digital-hydrant.db")
    if not "DH_DATABASE" in os.environ
    else os.environ.get("DH_DATABASE")
)

config = ConfigParser()

if os.path.isfile(ini_path):
    config.read(ini_path)
else:
    config.read(default_ini_path)

    os.makedirs(os.path.dirname(ini_path), exist_ok=True)
    with open(ini_path, "w") as configfile:
        config.write(configfile)

    os.chmod(ini_path, 0o600)

if not os.path.isfile(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, "w") as configfile:
        pass


updater = ConfigUpdater()
updater.read(ini_path)


def update_config(data, update_value=True):
    for section, value in data.items():
        if isinstance(value, dict):
            if not section in updater:
                updater.add_section(section)

            for option, option_value in value.items():
                if not option in updater[section] or (
                    updater[section][option].value != option_value and update_value
                ):
                    updater.set(section, option, option_value)

    updater.update_file()

    return updater.to_dict()


def get_sections(start):
    values = []
    for section in config.sections():
        if section.startswith(start):
            values.append(section)

    return values


def check_default_config():
    default_config = ConfigParser()
    default_config.read(default_ini_path)
    update_config(default_config._sections, False)
