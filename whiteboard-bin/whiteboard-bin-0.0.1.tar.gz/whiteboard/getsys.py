from sys import platform

def get_platform():
    if platform == 'linux':
        os_name = open('/etc/os-release').readlines()[0]
        if os_name.__contains__('Arch Linux'):
            return 'archlinux'
        else:
            print("Your Linux distribution is not supported.")
    else:
        return 'This program is currently only available for Linux systems.'