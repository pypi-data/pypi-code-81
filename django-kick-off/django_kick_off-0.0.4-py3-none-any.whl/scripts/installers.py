# Built-in 
import re
import subprocess

# Add parent path
import sys
sys.path.insert(0, re.findall('(^.+)/', sys.path[0])[0])

# Own modules
from conf import requirements
from cprint import cprint


# Upgrade pip
cprint.info('\nUpgrading pip... ')
command = 'python -m pip install --upgrade pip'
subprocess.run(command.split())
cprint.success('[Success]')

# Install requirements
for requirement in requirements.requirements_list:
    cprint.info(f'\nInstalling {requirement}... ')
    command = f'pip install {requirement}'
    effort = subprocess.run(command.split())
    if effort.returncode == 0:
        cprint.success('[Success]')
    else:
        cprint.error('[Error]')

cprint.info(f'\nAll modules installed ')
subprocess.run('pip list', shell=True)

# Start django project
project_name = sys.argv[1]
cprint.info(f'\nCreate the django project "{project_name}"... ')
command = f'django-admin startproject {project_name}'
subprocess.run(command.split())
cprint.success('[Success]')

# Run migrations
cprint.info(f'\nRunning migrations... ')
command = f'cd {project_name} && python3 manage.py migrate'
subprocess.run(command, shell=True)
cprint.success('[Success]')

# Start app Home
cprint.info(f'\nStarting app "home"... ')
command = f'cd {project_name} && python3 manage.py startapp home'
subprocess.run(command, shell=True)
cprint.success('[Success]')

# Add .editorconfig file
cprint.info(f'\nAdding .editorconfig to the project... ')
command = f'cp {sys.path[0]}/files/.editorconfig {project_name}/'
subprocess.run(command, shell=True)
cprint.success('[Success]')

# Set up app Home
cprint.info(f'\nSetting up app "home"... ')

# Templates
command = f'mkdir {project_name}/home/templates/ &&\
            mkdir {project_name}/home/templates/home/ &&\
            cp {sys.path[0]}/files/home/templates/home/main.html {project_name}/home/templates/home/'
subprocess.run(command, shell=True)

# Static
command = f'mkdir {project_name}/home/static/ &&\
            mkdir {project_name}/home/static/home/ &&\
            cp {sys.path[0]}/files/home/static/favicon.ico {project_name}/home/static/'
subprocess.run(command, shell=True)

# replace views.py, urls.py and context_processors.py
command = f'cp {sys.path[0]}/files/home/*.py {project_name}/home/'
subprocess.run(command, shell=True)
cprint.success('[Success]')

# Set up Core
cprint.info(f'\nSetting up core... ')
# replace urls.py
command = f'cp {sys.path[0]}/files/core/*.py {project_name}/{project_name}/'
subprocess.run(command, shell=True)

# Edit settings.py
new_lines = [
    (31, ""),
    (32, "APP_NAME = 'Project Name'"),
    (41, ""),
    (42, "    # Own Apps"),
    (43, "    'home',"),
    (69, "                'home.context_processors.settings',"),
]

# Open file, make a list and close it
with open(f'{project_name}/{project_name}/settings.py', 'r') as settings_file:
    settings_list = settings_file.read().split('\n')
    settings_file.close()

# Add new lines
for i, line in new_lines:
    settings_list.insert(i, line)

# Convert to string
setting_string = ''
for line in settings_list:
    setting_string += (line + '\n')

# Rewrite settings.py
with open(f'{project_name}/{project_name}/settings.py', 'w') as settings_file:
    settings_file.write(setting_string[:-1])

cprint.success('[Success]')
