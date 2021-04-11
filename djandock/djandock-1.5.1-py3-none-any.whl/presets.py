DJANGO_PROJECT_CREATE_COMMAND = 'cd {name} && cd venv && cd Scripts && "activate" && cd ../.. && django-admin startproject {name} .'
VIRTUALENV_DIR = 'venv'
PACKAGE_INSTALL_COMMAND = 'cd {name} && cd venv && cd Scripts && "activate" && pip install django && cd ../../ && pip freeze > requirements.txt'