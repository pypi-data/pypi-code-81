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
    hl,
    take_input
)
from .utils import (
    create_app_init_py,
    create_models_py,
    create_forms_py,
    create_routes_py,
    append_app_datas,
)


@click.group(cls=MultiCommand)
def startapp():
    pass


@startapp.command("startapp")
def startapp_command():
    if not in_virtualenv():
        raise Exception("You must be in virtual environment to run")
    
    processes = []
    process_ok(processes)

    # Taking app name
    app_name = take_input("Enter name for app:")

    # Creating app folder
    prj_name = PSMReader().get_config().get('PROJECT_NAME', None)
    if not prj_name :
        raise Exception("You deleted your project name from psm.json file. Please add it.")
    
    process_step(f"Creating {hl(join(prj_name, app_name))} folder...",
                create_folder(join(prj_name, app_name)))
    processes.append(f"Created {hl(join(prj_name, app_name))} folder")
    process_ok(processes)

    # Creating __init__.py
    process_step(f"Creating {hl(join(prj_name, app_name, '__init__.py'))}...",
                create_app_init_py(join(prj_name, app_name)))
    processes.append(f"Created {hl(join(prj_name, app_name, '__init__.py'))}")
    process_ok(processes)

    # Creating templates folder
    process_step(f"Creating {hl(join(prj_name, app_name, 'templates'))} folder...",
                create_folder(join(prj_name, app_name, 'templates')))
    processes.append(f"Created {hl(join(prj_name, app_name, 'templates'))} folder")
    process_ok(processes)
    
    # Creating models.py
    process_step(f"Creating {hl(join(prj_name, app_name, 'models.py'))}...",
                create_models_py(join(prj_name, app_name)))
    processes.append(f"Created {hl(join(prj_name, app_name, 'models.py'))}")
    process_ok(processes)

    # Creating forms.py
    process_step(f"Creating {hl(join(prj_name, app_name, 'forms.py'))}...",
                create_forms_py(join(prj_name, app_name)))
    processes.append(f"Created {hl(join(prj_name, app_name, 'forms.py'))}")
    process_ok(processes)

    # Creating routes.py
    process_step(f"Creating {hl(join(prj_name, app_name, 'routes.py'))}...",
                create_routes_py(prj_name,app_name))
    processes.append(f"Created {hl(join(prj_name, app_name, 'routes.py'))}")
    process_ok(processes)

    # Appending app datas to __init__.py
    process_step(f"Appending {app_name} modules to {hl(join(prj_name, '__init__.py'))}...",
                append_app_datas(prj_name, app_name))
    processes.append(f"Appended {app_name} modules to {hl(join(prj_name, '__init__.py'))}")
    process_ok(processes)

    # Appending app name to psm config
    psm = PSMReader()
    psm_config = psm.get_config()
    psm_config['APPS'].append(app_name)
    psm.set_config(psm_config)
    psm.write()

    # Output success message
    success_message(f"Successfully created {hl(app_name)}")
    info_message(f"Use {hl('psm run')} to run your application")
