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
    in_virtualenv,
    success_message,
    make_compatible,
    hl
)
from .utils import (
    create_static_folders,
    create_init_py,
    create_config_py,
    create_app_py,
    write_requirements,
    create_gitignore
)


@click.group(cls=MultiCommand)
def startproject():
    pass


@startproject.command("startproject")
def startproject_command():
    if not in_virtualenv():
        raise Exception("You must be in virtual environment to run")
    
    processes = []
    process_ok(processes)

    # Install PSM
    command_process_step(
        "Installing PSM...", "pip install --upgrade python-script-manager")
    processes.append("Installed PSM")
    process_ok(processes)

    # Create psm.json
    command_process_step("Initializing PSM...",
                        'psm init --template="blank"')
    processes.append("Initialized PSM")
    process_ok(processes)

    # Create config field
    psm = PSMReader('psm.json')
    psm_config = psm.get_config()
    psm_config["APPS"] = []
    psm_config["PROJECT_NAME"] = make_compatible(psm.get_name())
    psm.set_config(psm_config)
    psm.write()

    prj_name = psm_config["PROJECT_NAME"]

    # Creating requirements.txt
    process_step("Creating requirements.txt", write_requirements)
    processes.append("Created requirements.txt")
    process_ok(processes)

    # Installing requirements.txt
    command_process_step(f"Installing {hl('requirements.txt')}...",
                        'psm install && psm freeze')
    processes.append(f"Installed {hl('requirements.txt')}")
    process_ok(processes)

    # Creating main app folder
    process_step(f"Creating {hl(prj_name)} folder...",
                create_folder(prj_name))
    processes.append(f"Created {hl(prj_name)} folder")
    process_ok(processes)

    # Creating .gitignore
    process_step(f"Creating {hl('.gitignore')}...", create_gitignore)
    processes.append(f"Created {hl('.gitignore')}")
    process_ok(processes)

    # Creating app.py
    process_step(f"Creating {hl('app.py')}...", create_app_py(prj_name))
    processes.append(f"Created {hl('app.py')}")
    process_ok(processes)

    # Creating config.py
    process_step(f"Creating {hl('config.py')}...", create_config_py)
    processes.append(f"Created {hl('config.py')}")
    process_ok(processes)

    # Creating project __init__.py
    process_step(f"Creating {hl(join(prj_name,'__init__.py'))}...",
                create_init_py(prj_name))
    processes.append(f"Created {hl(join(prj_name,'__init__.py'))}")
    process_ok(processes)

    # Creating js, css, image folders
    process_step(f"Creating {hl(join(prj_name,'static'))} folder...",
                create_static_folders(prj_name))
    processes.append(f"Created {hl(join(prj_name,'static'))} folder")
    process_ok(processes)

    # Initializing DB
    command_process_step("Initializing database...", "flask db init")
    processes.append("Initialized database")
    process_ok(processes)

    # Commiting initial migration
    command_process_step("Commiting initial migration...",
                        'flask db migrate -m "initial"')
    processes.append("Commited initial migration")
    process_ok(processes)

    # Upgrading migration
    command_process_step("Upgrading migration...", "flask db upgrade")
    processes.append("Upgraded migration")
    process_ok(processes)

    # Initializing git
    command_process_step("Initializing git...", "git init")
    processes.append("Initialized git")
    process_ok(processes)

    # Output success message
    success_message(f"Successfully created project {hl(prj_name)}")
    info_message(f"Use {hl('psm run')} to run your application")