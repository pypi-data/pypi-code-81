import os
from list import get_commands, get_packages, get_standalones, get_dependencies, get_orphans
from interface import banner, footer

def main():
    commands = get_commands()

    # Print the banner
    print(banner())

    # Print the package manager name
    print('-=-=- ' + commands[0] + ' -=-=-')
    print('You have ' + get_packages() + ' total packages. (' + commands[1] + ')')
    print('You have ' + get_standalones() + ' standalone packages. (' + commands[2] + ')')
    print('You have ' + get_dependencies() + ' dependencies. (' + commands[3] + ')')
    print('You have ' + get_orphans() + ' orphaned packages. (' + commands[4] + ')')
    
    print(footer())

main()