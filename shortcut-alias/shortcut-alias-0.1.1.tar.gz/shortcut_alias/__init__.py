from sys import path
import yaml
import pathlib

__author__ = "Matt Limb <matt.limb17@gmail.com>"

SETTINGS = {
    "show_command": True,
    "show_reason": True,
    "show_output": True,
    "show_output_header": True,
    "show_skip": True,
    "colour": True
}

def load_settings(filepath):
    filepath = pathlib.Path(filepath)
    
    if filepath.exists():
        with filepath.open("r") as f:
            SETTINGS.update(
                yaml.safe_load(f.read())
            )
    else:
        with filepath.open("w") as f:
            f.write(
                yaml.safe_dump(SETTINGS, indent=2)
            )

def setup_settings(filepath):
    root = pathlib.Path(filepath)
    config = pathlib.Path(root, "shortcut.d")

    root.mkdir()
    config.mkdir()

    with pathlib.Path(root, "settings.yaml").open("w") as f:
        f.write(
            yaml.safe_dump(SETTINGS, indent=2)
        )