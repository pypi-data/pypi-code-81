# -*- coding: utf-8 -*-
"""
Module Description.


"""
from pathlib import Path

import yaml

DIR = Path(__file__).parent.parent
SETTINGS_PATH = Path(DIR).absolute()


def saveSettings(settings: dict,
                 settings_path: Path = SETTINGS_PATH,
                 sort_keys: bool = False) -> None:
    settings_path.mkdir(exist_ok=True, parents=True)
    with open(settings_path / 'settings.yaml', 'w') as f:
        yaml.dump(settings, f, sort_keys=sort_keys)


def loadSettings(settings_path: Path = SETTINGS_PATH) -> dict:
    if (not (settings_path / 'settings.yaml').exists()):
        saveSettings({})
    with open(settings_path / 'settings.yaml', 'r') as f:
        settings = yaml.full_load(f)
    return settings


def updateSettings(settings: dict, update: dict):
    settings.update(update)
    saveSettings(settings)
