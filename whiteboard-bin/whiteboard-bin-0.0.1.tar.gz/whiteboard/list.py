from os import popen
from getsys import get_platform

# command structure: [count total packages, count standalones, count dependencies, count orphans]
commands_list = {
    'archlinux': ['pacman', 'pacman -Q', 'pacman -Qe', 'command unavailable', 'pacman -Qtdq'],
    'debian': ['dpkg', 'a', 'b', 'c', 'd']
}

def get_commands():
    return commands_list.get('archlinux')

commands = get_commands()

def get_packages():
    return str(len(popen(get_commands()[1]).read().splitlines()))

def get_standalones():
    return str(len(popen(get_commands()[2]).read().splitlines()))

def get_dependencies():
    return str(len(popen(get_commands()[1]).read().splitlines()) - len(popen(get_commands()[2]).read().splitlines()))

def get_orphans():
    return str(len(popen(get_commands()[4]).read().splitlines()))