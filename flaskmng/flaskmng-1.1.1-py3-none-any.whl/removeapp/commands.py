from os.path import join
import click
from python_script_manager.package import PSMReader
from ..utils import (
    MultiCommand,
    command_process_step,
    info_message,
    process_ok,
    process_step,
    create_folder,
    success_message,
    make_compatible,
    hl,
    take_input
)
from .utils import (
    remove_app,
    remove_app_imports
)


# @click.group(cls=MultiCommand)
# def removeapp():
#     pass
from ..__main__ import main

@main.command("removeapp")
def removeapp_command():
    """Remove app in project"""
    psm = PSMReader()
    prj_name = psm.get_config().get('PROJECT_NAME', None)
    app_list = psm.get_config().get('APPS', None)
    processes = []
    process_ok(processes)

    # Taking app name to remove
    app_name = take_input("Enter name of app to remove:")

    # Removing app folder
    if not prj_name :
        raise Exception("You deleted your project name from psm.json file. Please add it.")
    if not app_name in app_list:
        raise Exception("Your app name is not in app list")
    process_step(f"Removing {hl(join(prj_name, app_name))} folder...",
                remove_app(join(prj_name, app_name)))
    processes.append(f"Removed {hl(join(prj_name, app_name))} folder")
    process_ok(processes)

    # Removing app name from psm.json
    psm_config = psm.get_config()
    psm_config['APPS'].remove(app_name)
    psm.set_config(psm_config)
    psm.write()

    # Removing app modules from __init__.py
    process_step(f"Removing imports of {hl(app_name)} from {hl(join(prj_name, '__init__.py'))}...",
                remove_app_imports(prj_name, app_name))
    processes.append(f"Removed imports of {hl(app_name)} from {hl(join(prj_name, '__init__.py'))}")
    process_ok(processes)

    # Output success message
    success_message(f"Successfully removed {hl(app_name)}")
    info_message(f"Use {hl('psm run')} to run your application")
