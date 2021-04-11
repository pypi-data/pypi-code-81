import venv, os
from presets import VIRTUALENV_DIR, PACKAGE_INSTALL_COMMAND

def create_virtual_env(directory, install_libs=True):
    builder = venv.EnvBuilder(with_pip=True, upgrade_deps=True)
    builder.create(os.path.join(os.getcwd(), directory, VIRTUALENV_DIR))

    if install_libs:
        # Attempt to enter the virtual environment and install required scripts there.
        # Might be tricky since Windows and Linux differ in activating the virtualenv
        
        code = os.system(PACKAGE_INSTALL_COMMAND.format(name=directory))
        if code == 0:
            print('\tDjango installed successfully')
            return
        print('\tCouldn\'t install Django. The following steps may fail')

    